#!/bin/bash
# entrypoint.sh

# Wait for the PostgreSQL service to be available
until psql -h "$DB_HOST" -U "$DB_USER" -c '\q'; do
  >&2 echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done

# Run the database setup script
./setup_db.sh

# Start the Flask application
exec flask run --host=0.0.0.0
