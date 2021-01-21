#!/bin/sh
# Full install process from fresh os
# Wezley 3

# Install python packages
apt-get install -y python3
python3 -m pip install -U pip
python3 -m pip install requests speedtest-cli

# Install required packages
apt-get install -y apache2 php libapache2-mod-php php7.3-sqlite3

# Allow php to access user directories
a2enmod userdir

# Restart apache to update settings
systemctl restart apache2

# Create database for php
mkdir -p /srv/databases/sst
chown -R www-data. /srv/databases/sst
touch /srv/databases/sst/results.db

chmod 776 /srv/databases/sst
chmod 664 /srv/databases/sst/results.db

cp ./html /var/www/html/simple_speed_test

echo "Data can now be viewed at http://127.0.0.1/simple_speed_test"
echo "Data can be uploaded to http://127.0.0.1/simple_speed_test/php/post_results.php"
