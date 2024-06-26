from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import requests
import subprocess
import os
from load_config import get_proxmox_config, get_hpe_ilo_config

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(50), nullable=False)
    user = db.Column(db.String(50), nullable=False)
    api_key = db.Column(db.String(200), nullable=False)

class VMConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vmid = db.Column(db.String(50), nullable=False)
    target_node = db.Column(db.String(50), nullable=False)

# Initialize the database
db.create_all()

proxmox_config = get_proxmox_config()
hpe_ilo_config = get_hpe_ilo_config()

# Get node statistics using Proxmox API key
def get_node_stats():
    headers = {"Authorization": f"PVEAPIToken={proxmox_config['api_key']}"}
    response = requests.get(f"{proxmox_config['api_url']}/nodes", headers=headers, verify=False)
    return response.json()['data']

# Power on server via iLO using API key
def power_on_server(ip):
    api_key = hpe_ilo_config[ip]
    cmd = f"ipmitool -I lanplus -H {ip} -U {api_key} chassis power on"
    subprocess.run(cmd, shell=True)

# Migrate VM using Proxmox API key
def migrate_vm(vmid, target_node):
    headers = {
        "Authorization": f"PVEAPIToken={proxmox_config['api_key']}"
    }
    data = {"target": target_node}
    requests.post(f"{proxmox_config['api_url']}/nodes/node1/qemu/{vmid}/migrate", headers=headers, data=data, verify=False)

# Default rout leading to the index that will show the overview page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/status')
def status():
    node_stats = get_node_stats()
    return jsonify(node_stats)

@app.route('/poweron', methods=['POST'])
def poweron():
    data = request.json
    power_on_server(data['ip'])
    return jsonify({"status": "success"})

@app.route('/migrate', methods=['POST'])
def migrate():
    data = request.json
    migrate_vm(data['vmid'], data['target_node'])
    return jsonify({"status": "success"})

# Flask Config for the configuration page
@app.route('/config', methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        # Save configuration to the database
        server = Server(ip=request.json['ip'], user=request.json['user'], api_key=request.json['api_key'])
        db.session.add(server)
        db.session.commit()
        return jsonify({"status": "success"})
    else:
        # Load configuration from the database
        servers = Server.query.all()
        return jsonify([{"ip": server.ip, "user": server.user, "api_key": server.api_key} for server in servers])

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
