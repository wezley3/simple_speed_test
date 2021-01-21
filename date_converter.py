#!/usr/bin/env python3
# Conver 2 digit dates to 4
# by wezley3
# 1/19/2021

import datetime
import sqlite3
import time
import sys

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

if __name__ == "__main__":

  db_location = None

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

  # Check for database, if none provided default to verbose settings
  if db_location is None:
    print()
    print("No database location provided")
    exit()

  # Select all unique dates from db
  query = "select ins_date from results group by ins_date;"
  results = read_db(db_location, query)

  # Update all dates with new 4 digit date
  query_template = "update results set ins_date = '%s' where ins_date = '%s'"
  for bad_date in results:
    new_date = "20" + bad_date[0]
    query = (query_template % (new_date, bad_date[0]))
    edit_db(db_location, query)
