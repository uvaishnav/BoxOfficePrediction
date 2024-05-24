# Use a base image with Python (e.g., python:3.9-slim)
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Update the package list and install necessary system dependencies
RUN apt-get update -y && \
    apt-get install -y gcc python3-dev && \
    apt-get install -y awscli

# Install the Python dependencies
RUN pip install -r requirements.txt

# Expose port 8080
EXPOSE $PORT

# Specify the command to run your application
CMD gunicorn --workers=4 --bind 0.0.0.0:$PORT app:app
