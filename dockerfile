# Use the official Python image from the Docker Hub
FROM python:3.11

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file
COPY ./HA-Service/requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY HA-Service /app/HA-Service

# Set environment variables for the database connection
ENV DB_HOST=db
ENV DB_PORT=5432
ENV DB_NAME=config_db
ENV DB_USER=config_user
ENV DB_PASSWORD=supersecret

# Set enviroment variables in the config file so that the Flask app can connect to the database
RUN sed -i "s|DB_HOST|${DB_HOST}|g" /app/HA-Service/config.py
RUN sed -i "s|DB_PORT|${DB_PORT}|g" /app/HA-Service/config.py
RUN sed -i "s|DB_NAME|${DB_NAME}|g" /app/HA-Service/config.py
RUN sed -i "s|DB_USER|${DB_USER}|g" /app/HA-Service/config.py
RUN sed -i "s|DB_PASSWORD|${DB_PASSWORD}|g" /app/HA-Service/config.py

# Set environment variables for the Flask app
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Copy the setup script
COPY ./HA-Service/init_db.sh .

# Make the setup script executable
RUN chmod +x init_db.sh

# Use an entrypoint script to initialize the database and start the Flask app
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]

# Expose the port that the Flask app runs on
EXPOSE 5000
