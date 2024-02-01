#!/usr/bin/env bash
# Bash script that sets up your web servers for the deployment of web_static

# Install Nginx if it not installed
if ! dpkg -s nginx &> /dev/null;
then
    sudo apt-get update;
    sudo apt-get -y install nginx;
    sudo ufw allow 'Nginx HTTP';
fi;

# Create the folder /data/ with all subfolders (recursively)
sudo mkdir -p /data/web_static/releases/test/;
sudo mkdir -p /data/web_static/shared/;

# Create a fake HTML file /data/web_static/releases/test/index.html
echo 'successful test http' | sudo tee /data/web_static/releases/test/index.html;

# Create a symbolic link /data/web_static/current linked to the /data/web_static/releases/test/ folder
sudo rm -rf /data/web_static/current;
sudo ln -s /data/web_static/releases/test/ /data/web_static/current;
sudo chown -R ubuntu:ubuntu /data/;

# Update the Nginx configuration to serve the content of /data/web_static/current/ to hbnb_static
sudo sed -i '/^.*server_name _;$/a \\n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default;
sudo service nginx restart;
