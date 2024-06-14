#!/bin/bash
# setup_db.sh

DB_HOST=${DB_HOST:-localhost}
DB_PORT=${DB_PORT:-5432}
DB_NAME=${DB_NAME:-config_db}
DB_USER=${DB_USER:-config_user}
DB_PASSWORD=${DB_PASSWORD:-supersecret}

# Create the database and user
psql -h $DB_HOST -p $DB_PORT -U postgres <<EOSQL
CREATE DATABASE $DB_NAME;
CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
EOSQL

# Create tables for Proxmox and HPE Ilo configurations
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME <<EOSQL
CREATE TABLE proxmox_config (
    id SERIAL PRIMARY KEY,
    api_url TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE hpe_ilo_config (
    id SERIAL PRIMARY KEY,
    ilo_url TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);
EOSQL
