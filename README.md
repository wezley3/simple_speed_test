# simple_speed_test
Runs a simple speed test and logs the results to sqlite3 and post requests.

Required imports 

pip3 install sqlite3 requests speedtest-cli


# Command line arguments

usage: main.py [-h] [-v] [-V] [-d [DATABASE [DATABASE ...]]]

               [-u [URL [URL ...]]] [-p [PING]] [-s [SLEEP]] [-t [TESTS]]

Simple Speed Test is designed to run a quick test on the nearest speed test

servers. The results can then be loged to a database or uploaded to a server

with POST. Other options may be set to help in diagnosing problems such as

longer pings or multiple tests.

optional arguments:

  -h, --help            show this help message and exit
  
  -v, --verbose         Speed test verbose option
  
  -V, --very_verbose    All verbose option
                          
  -p [PING], --ping [PING]    number of ping attempts
                        
  -t [TESTS], --tests [TESTS] number of tests to be ran
  
  -s [SLEEP], --sleep [SLEEP] number of seconds between tests
  
  -u [URL [URL ...]], --url [URL [URL ...]] urls to upload data to
  
  -d [DATABASE [DATABASE ...]], --database [DATABASE [DATABASE ...]]  databases to upload data to


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
