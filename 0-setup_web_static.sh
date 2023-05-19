#!/bin/bash

# Check if Nginx is installed
if ! [ -x "$(command -v nginx)" ]; then
  echo "Nginx is not installed. Installing..."
  apt-get install nginx
fi

# Create the /data/ directory
if ! [ -d /data ]; then
  mkdir /data
fi

# Create the /data/web_static/ directory
if ! [ -d /data/web_static ]; then
  mkdir /data/web_static
fi

# Create the /data/web_static/releases/ directory
if ! [ -d /data/web_static/releases ]; then
  mkdir /data/web_static/releases
fi

# Create the /data/web_static/shared/ directory
if ! [ -d /data/web_static/shared ]; then
  mkdir /data/web_static/shared
fi

# Create the /data/web_static/releases/test/ directory
if ! [ -d /data/web_static/releases/test ]; then
  mkdir /data/web_static/releases/test
fi

# Create a fake HTML file /data/web_static/releases/test/index.html
echo "This is a test page." > /data/web_static/releases/test/index.html

# Create a symbolic link /data/web_static/current linked to the /data/web_static/releases/test/ folder
if [ -L /data/web_static/current ]; then
  rm /data/web_static/current
fi
ln -s /data/web_static/releases/test /data/web_static/current

# Give ownership of the /data/ directory to the ubuntu user AND group
chown -R ubuntu:ubuntu /data

# Update the Nginx configuration to serve the content of /data/web_static/current/ to hbnb_static
# Use alias inside your Nginx configuration
# Tip

# Restart Nginx
service nginx restart

# Exit successfully
exit 0
