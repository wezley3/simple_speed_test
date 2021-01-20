#!/bin/sh
# Help to set up apache2 for php
# wezley3

# Install required packages
apt-get install -y apache2 php libapache2-mod-php php7.3-sqlite3

# Allow php to access user directories
a2enmod userdir

# Restart apache to update settings
systemctl restart apache2

# Print info about linking html package

echo "Please move or link html package to /var/www/"
echo "Example: ln -s /home/user/simple_speed_test/html /var/www/simple_speed_test"
