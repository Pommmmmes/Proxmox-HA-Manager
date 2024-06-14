# load_config.py
import psycopg2
from config import config

def get_proxmox_config():
    conn = psycopg2.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD
    )
    cur = conn.cursor()
    cur.execute("SELECT api_url, username, password FROM proxmox_config LIMIT 1;")
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return {'api_url': row[0], 'username': row[1], 'password': row[2]}
    return None

def get_hpe_ilo_config():
    conn = psycopg2.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD
    )
    cur = conn.cursor()
    cur.execute("SELECT ilo_url, username, password FROM hpe_ilo_config LIMIT 1;")
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return {'ilo_url': row[0], 'username': row[1], 'password': row[2]}
    return None
