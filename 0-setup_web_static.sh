#!/usr/bin/env bash
# script that sets up web servers for the deployment of web_static

# Check if Nginx is already installed
if ! command -v nginx &> /dev/null; then
    sudo apt-get update
    sudo apt-get -y install nginx
    sudo ufw allow 'Nginx HTTP'
fi

# Create directories
sudo mkdir -p /data/web_static/releases/test/

# Create a fake HTML file
echo "<html>
 <head>
 </head>
 <body>
    Holberton School
 </body>
</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create a symbolic link
sudo ln -s -f /data/web_static/releases/test/ /data/web_static/current

# Change ownership
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
sudo sed -i '/listen 80 default_server/a location /hbnb_static { alias /data/web_static/current/;}' /etc/nginx/sites-enabled/default

# Restart Nginx
sudo service nginx restart

# Exit with success status
exit 0
