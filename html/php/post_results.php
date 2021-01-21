<?php

# Build all tables exclusive to this database 
function build_tables($db_location){

  $host_table_query = "create table host(id int primart key not null, url text not null);";
  $results_table_query = "create table results(id int not null, download real, upload real, ping_min real, ping_avg real, ping_max real, ping_mdev real, distance real, ins_date date, FOREIGN KEY(id) references host(id));";

  create_table($db_location, 'results', $results_table_query, $force_exit);
  create_table($db_location, 'host', $host_table_query, $force_exit);

}

function create_table($db_location, $table_name, $insert_query, $force_exit){

  # Check if the table exsists
  $check_table_query = sprintf("select name from sqlite_master where type='table' and name = '%s';", $table_name);
  $db = new SQLite3($db_location);
  $results = $db->query($check_table_query)->fetchArray();
  if($results != NULL)
    return True;# if table exsists

  # Create the table and run again to varify table exsists and return true
  if ($insert_query != NULL and $forece_exit == False){
    $db->exec($insert_query);
    $db->close();
    return create_table($db_location, $table_name, $insert_query, $forece_exit);
  }

  return False;# if no table was created


}


# Start

# Check all needed data was included inside the upload reject if any are missing
$keys = ['download','upload','ping', 'id', 'url', 'distance'];
foreach($keys as $key){
  if(!array_key_exists($key, $_POST)){
    echo "Invalid post data missing key:";
    echo $key;
    exit();
  }
}

# Fetch data out of post request
$results = $_POST;
$ping = json_decode($results['ping'], true);

# Build querys to insert data into database
$results_query = sprintf("insert into results(id, download, upload, ping_min, ping_avg, ping_max, ping_mdev, distance, ins_date)values(%d, %0.3f, %0.3f, %0.3f, %0.3f, %0.3f, %0.3f, %0.3f, '%s');", $results['id'], $results['download'], $results['upload'], $ping['min'], $ping['avg'], $ping['max'], $ping['mdev'], $results['distance'], $results['ins_date']);

$host_query = sprintf("insert into host(id, url) select %d, '%s' where not exists(select 1 from host where id = %d);", $results['id'], $results['url'], $results['id']);

# Insert the data into the database
$db_location = "/srv/databases/sst/results.db";
build_tables($db_location);
$db = new SQLite3($db_location);
$db->exec($results_query);
$db->exec($host_query);
$db->close();

echo "Data uploaded successfully";

?>
