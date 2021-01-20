#!/usr/bin/env python3
# Simple program to test net speeds and log them to a database
# by wezley3
# 1/18/2021

import subprocess 
import speedtest
import datetime
import sqlite3
import time
import sys

global verbose
global current_date

# simple sqlite3 edit command
def edit_db(db_location, query):
  conn = sqlite3.connect(db_location)
  db = conn.cursor()
  db.execute(query)
  conn.commit()
  conn.close()

# simple sqlite3 read command
def read_db(db_location, query):
  conn = sqlite3.connect(db_location)
  db = conn.cursor()
  result = db.execute(query)
  return_list = []
  for item in result.fetchall():
    return_list.append(item)
  conn.close()
  return return_list

# Creates db table if one does not exsist
def create_db_table(db_location, table_name, insert_query=None, force_exit=False):

  # Check if table all ready exsists
  query = ("select name from sqlite_master where type='table' and name='%s';" % (table_name))
  result = read_db(db_location, query)
  if len(result) > 0:
    return True

  # If a create table query was provided and force_exit is False add table
  if insert_query is not None and force_exit is False:
    edit_db(db_location, insert_query)
    return create_db_table(db_location, table_name, insert_query, True)

  return False # If no table was created

# Information to create database tables if needed
def build_tables(db_location):

  host_table_query = "create table host(id int primary key not null, url text not null);"
  results_table_query = "CREATE TABLE results(id int not null, download real, upload real, ping_min real, ping_avg real, ping_max real, ping_mdev real, distance real, ins_date date, FOREIGN KEY(id) references host(id));"

  create_db_table(db_location, "host", host_table_query)
  create_db_table(db_location, "results", results_table_query)

# Log the results from a speed test
def log_result(db_name, result):

  # Store id and server url if needed
  id_query = ("insert into host(id, url) select %d, '%s' where not exists(select 1 from host where id = %d);" % (result['id'], result['url'], result['id']));

  # Store all speed test results
  ping = result['ping']
  results_query = ("insert into results(id, download, upload, ping_min, ping_avg, ping_max, ping_mdev, distance, ins_date)values(%d, %0.3f, %0.3f, %0.3f, %0.3f, %0.3f, %0.3f, %0.3f, '%s');" % (result['id'], result['download'], result['upload'], ping['min'], ping['avg'], ping['max'], ping['mdev'], result['distance'], current_date))

  # Insert info into db
  edit_db(db_location, id_query)
  edit_db(db_location, results_query)

# To be added
def traceroute(input_ip):
  output = subprocess.check_output("traceroute " + input_ip, shell=True).decode("utf-8")

  lines = []
  for line in output.split("\n"):
    lines.append(line.split("  "))

  route_list = []
  for i in range(1, len(lines) - 1):
    if len(lines[i]) != 5:
      continue

    line_info = {}

    ip_info = lines[i][1].split(" ")
    line_info['url'] = ip_info[0]
    line_info['ip'] = ip_info[1][1:len(ip_info[1]) - 1]

    ping = []
    for m in range(2,5):
      ping.append(float(lines[i][m].split(" ms")[0]))
    line_info['ping'] = ping
    route_list.append(line_info)

  return route_list

# Run a quick ping on given ip address and return results
def quick_ping(input_ip, ping_attempts=3):

  # run ping command on shell
  command = ("ping %s -c %d" % (input_ip, ping_attempts))
  output = subprocess.check_output(command, shell=True).decode("utf-8")

  # Format the line
  output_lines = output.split("\n")

  # take last line
  info_line = output_lines[len(output_lines) - 2]

  # trim last line into pieces by time
  info_line = info_line.split(" = ")[1]
  info_line = info_line[:info_line.find(" ms")]
  split_info = info_line.split("/")

  # Store results in a dictionary
  results = {}
  results['min'] = float(split_info[0])
  results['avg'] = float(split_info[1])
  results['max'] = float(split_info[2])
  results['mdev'] = float(split_info[3])

  return results

# Get a list of servers from speedtest servers and format wanted information
def get_server_list(s=speedtest.Speedtest()):

  # get list of servers
  servers = []
  server_results = s.get_servers(servers)

  # store all server info into a list sorted by distance
  server_list = []
  for server_key in sorted(server_results.keys()):

    cur_server = server_results[server_key][0]

    server_info = {}
    server_info['location'] = cur_server['name']
    server_info['distance'] = cur_server['d'] 
    server_info['url'] = cur_server['url']
    server_info['host'] = cur_server['host']
    server_info['id'] = cur_server['id']

    server_list.append(server_info)

  return server_list

# Test the speeds of a given server and log the results into the provided database
def test_server(db_location, server, ping_attempts):

  # Get server for ping and strip port number off
  ping_url = server['host'] 
  ping_url = ping_url[:len(ping_url) - 5]

  global verbose
  if verbose is True:
    print()
    print("Server:", ping_url)

  # Run ping on server
  ping_results = quick_ping(ping_url, ping_attempts)

  # Select specific server for testing
  servers = []
  servers.append(server['id'])
  s.get_servers(servers)

  # Store results into a dict and insert it into master list
  results = {}
  results['id'] = int(server['id'])
  results['url'] = ping_url
  results['distance'] = float(server['distance'])
  results['ping'] = ping_results

  if verbose is True:
    print("Distance from server: %0.3f KM" % (results['distance']))
    print("Avg ping over %d attempts: %0.3f ms" % (ping_attempts, results['ping']['avg']))

  # Test download speed
  results['download'] = float(s.download())
  if verbose is True:
    print("Download speed: %0.3f Mb" % (results['download'] / 1000000))

  # Test upload speed
  results['upload'] = float(s.upload())
  if verbose is True:
    print("Upload speed: %0.3f Mb" % (results['upload'] / 1000000))


  # Log results to database if provided
  if db_location is not None:
    log_result(db_location, results)

  return results

if __name__ == "__main__":

  global verbose
  global current_date

  # Default variables
  verbose = False
  db_location = None
  ping_attempts = 3
  servers2test = 2
  test_delay = 30

  # Check for system arguments
  if len(sys.argv) > 1:

    # Loop through all arguments seatching for values to set
    for i in range(1, len(sys.argv)):

      # Skips non command inputs
      if sys.argv[i][0] is not '-':
        continue

      # Set database location
      if sys.argv[i] == "-d":
        if i + 1 < len(sys.argv):
          db_location = sys.argv[i + 1]

      # Set ping attemts
      if sys.argv[i] == "-p":
        if i + 1 < len(sys.argv):
          ping_attempts = int(sys.argv[i + 1])

      # Set servers2test
      if sys.argv[i] == "-t":
        if i + 1 < len(sys.argv):
          servers2test = int(sys.argv[i + 1])

      # Set test_delay 
      if sys.argv[i] == "-s":
        if i + 1 < len(sys.argv):
          test_delay = int(sys.argv[i + 1])

      # Set global verbose setting
      if sys.argv[i] == "-v":
        verbose = True
  
      # Print help otions then exit
      if sys.argv[i] == "-h" or sys.argv[i] == "--help":
        print("'-v' to enable verbose option")
        print("'-d database_location.db' to set database")
        print("'-p 4' to set ping attemts to 4: default 3")
        print("'-t 4' to set servers to test to 4: default 2")
        print("'-s 60' to set sleep between runs to 60sec: default 30sec")
        exit()


  # Check for database, if none provided default to verbose settings
  if db_location is None:
    print()
    print("No database location provided")
    print("Use -h or --help for help")
    print("Defaulting to verbose")
    verbose = True
  else:
    # Build the tables for database if needed
    build_tables(db_location)


  # Print information when inside verbose
  if verbose is True:
    print()
    print("Testing information")
    print("Verbose:", verbose)
    print("Database:", db_location)
    print("Ping attempts:", ping_attempts)
    print("Servers to test:", servers2test)
    print("Delay between tests", test_delay)
    print()


  # Store common datetime for all tests
  current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

  if verbose is True:
    print("Starting tests at", current_date)

  # Link to speed test class
  s = speedtest.Speedtest()

  # Get the list of servers to test
  server_list = get_server_list(s)

  # Create master list for results
  speed_test_results = []


  if verbose is True:
    print("Testing top %d servers" % (servers2test))

  # Test given number of servers and sleep given time between test
  for i in range(0, servers2test):
    if i is not 0:
      if verbose is True:
        print("\nResting for %d sec" % (test_delay))
      time.sleep(test_delay)
    test_server(db_location, server_list[i], ping_attempts)
