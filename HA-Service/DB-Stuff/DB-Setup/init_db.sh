#!/bin/bash

DATABASE_URL="postgresql://user:password@localhost:5432/mydatabase"

psql $DATABASE_URL <<EOF
CREATE TABLE base_config (
    id SERIAL PRIMARY KEY,
    key VARCHAR(255) UNIQUE NOT NULL,
    value TEXT NOT NULL
);

CREATE TABLE proxmox_config (
    id SERIAL PRIMARY KEY,
    key VARCHAR(255) UNIQUE NOT NULL,
    value TEXT NOT NULL
);

CREATE TABLE hpe_ilo_config (
    id SERIAL PRIMARY KEY,
    key VARCHAR(255) UNIQUE NOT NULL,
    value TEXT NOT NULL
);
EOF

echo "Database initialized successfully."
