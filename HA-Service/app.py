from flask import Flask, request, jsonify, render_template, redirect, url_for
import requests
import subprocess
import json
import os

app = Flask(__name__)
app.config.from_pyfile('config.py')

# Get node statistics using Proxmox API key
def get_node_stats():
    headers = {"Authorization": f"PVEAPIToken={app.config['PROXMOX_API_KEY']}"}
    response = requests.get(f"{app.config['PVE_API_URL']}/nodes", headers=headers, verify=False)
    return response.json()['data']

# Power on server via iLO using API key
def power_on_server(ip, api_key):
    headers = {"Authorization": f"Bearer {api_key}"}
    cmd = f"ipmitool -I lanplus -H {ip} -U {api_key} chassis power on"
    subprocess.run(cmd, shell=True)

# Migrate VM using Proxmox API key
def migrate_vm(vmid, target_node):
    headers = {
        "Authorization": f"PVEAPIToken={app.config['PROXMOX_API_KEY']}"
    }
    data = {"target": target_node}
    requests.post(f"{app.config['PVE_API_URL']}/nodes/node1/qemu/{vmid}/migrate", headers=headers, data=data, verify=False)

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
    power_on_server(data['ip'], data['api_key'])
    return jsonify({"status": "success"})

@app.route('/migrate', methods=['POST'])
def migrate():
    data = request.json
    migrate_vm(data['vmid'], data['target_node'])
    return jsonify({"status": "success"})

@app.route('/config', methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        # Save configuration
        with open('config.json', 'w') as config_file:
            json.dump(request.json, config_file)
        return jsonify({"status": "success"})
    else:
        # Load configuration
        if os.path.exists('config.json'):
            with open('config.json', 'r') as config_file:
                config = json.load(config_file)
            return jsonify(config)
        else:
            return jsonify({})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
