# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the entire project into the container at /app
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Install Nginx, Node.js, and npm
RUN apt-get update && \
    apt-get install -y nginx nodejs npm && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install frontend dependencies
WORKDIR /app/frontend
RUN npm install

# Back to the root app directory
WORKDIR /app

# Setup Nginx configuration
# Ensure the nginx.conf file is available at the correct relative path
COPY ./config/nginx.conf /etc/nginx/nginx.conf

# Remove the default server definition
RUN rm /etc/nginx/sites-enabled/default

# Copy the frontend build into the Nginx serve directory
# This assumes that 'frontend' directory contains the built project ready to serve
# If your frontend needs a build step (e.g., `npm run build`), ensure this happens before this COPY command
COPY . /var/www/html/

# Expose port 80 for the web server
EXPOSE 80

# Environment variables can be defined if needed
ENV NAME World

# Use CMD to start Nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]
