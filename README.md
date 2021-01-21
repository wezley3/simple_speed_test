# simple_speed_test
Runs a simple speed test and logs the results to sqlite3 and post requests.

Required imports 

pip3 install sqlite3 requests speedtest-cli


# Command line arguments

'-h' or '--help' to print Help

'-v' to enable Verbose: default False

'-d speed_test.db' to set Database location: default None

'-u http://127.0.0.1/sst/php/post_results.php' to set custom upload ulr

'-U' to default to statz.live

'-p 4' sets Ping attempts to 4: default 3

'-t 4' to set servers to Test to 4: default 2

'-s 45' to set Sleep beween tests to 45sec: default 30sec


# Examples 

cli example

Tests one server with four pings and logs results to test.db

./main.py -v -d test.db -p 4 -t 1

cron command example

Tests three servers with a sixty seconds delay between tests and logs results to a database

/home/user_name/simple_speed_test/main.py -d /home/user_name/databases/speed_test.db -t 3 -s 60

Test default settings and upload data to custom post server

./main.py -u http://127.0.0.1/simple_speed_test/php/post_results.php

# Web Setup

Run the setup_apache.sh to handle installing and setting apache2 settings

Link html file to /var/www/html/

Example: 'ln -s /home/user/programs/simple_speed_test/html /var/www/html/simple_speed_test'

# Other Information

Database and tables are created at runtime if needed.

Designed and tested on debian os.

Statz.live is an in progress data viewing website. Data will be logged to server with -U command and will be able to be viewed by distances from test servers in the future.
