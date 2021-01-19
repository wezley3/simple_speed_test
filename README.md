# simple_speed_test
Runs a simple speed test and logs the results to sqlite3.

Required imports 

pip3 install sqlite3 speedtest-cli


# Command line arguments

'-h' or '--help' to print Help

'-v' to enable Verbose: default False

'-d speed_test.db' to set Database location: default None

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


# Other Information

Database and tables are created at runtime if needed.

Designed and tested on debian os.
