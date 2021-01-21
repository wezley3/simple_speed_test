<?php

# Build query based on key value
function get_query($key, $ins_time){

  # Templates to sprintf into later
  $day_query_template = "select download, upload, ping_avg from results where strftime('%s', ins_date) = '%s' and strftime('%s', ins_date) = '%s';";

  $life_query_template = "select avg(download) as download, avg(upload) as upload, avg(ping_avg) as ping_avg from results where strftime('%s', ins_date) = '%s';";

  # Build querys based on key and time provided
  switch($key){
    case 'today':
      return sprintf($day_query_template, "%H", $ins_time, "%d", date('d'));

    case 'yeasterday':
      return sprintf($day_query_template, "%H", $ins_time, "%d", date('d') - 1);

    case 'life':
      return sprintf($life_query_template, "%H", $ins_time);

  };
}

# Get all test results from the provided database
function get_all_test_results($db_location){


  # Setting up return values

  # Used in proper conversion from bits to megabits
  $mb = 1048576;

  # Create a dictionary to store results
  $r_value = array();
  $keys = ['download', 'upload', 'ping'];

  # Build return structure based on keys above
  foreach($keys as $key){
    $r_value[$key] = array();
    $r_value[$key]['today'] = array();
    $r_value[$key]['yeasterday'] = array();
    $r_value[$key]['life'] = array();
  }


  # Retrieving information from the databse

  # Open link to database
  $db = new SQLite3($db_location);

  # Loop through 24 hours worth of time
  for($i = 0; $i < 24; ++$i){

    if($i < 10)
      $ins_time = sprintf('0%d', $i);
    else
      $ins_time = sprintf('%d', $i);

    # For each key in the list
    $keys = ['today', 'yeasterday', 'life'];
    foreach($keys as $key){

      # Build query and fetch data from db based on key type
      $results = $db->query(get_query($key, $ins_time))->fetchArray();

      if($results != NULL){

        # Trim strings down and divide for Mb's
        $download = (float)sprintf("%0.3f", $results['download'] / $mb);
        $upload = (float)sprintf("%0.3f", $results['upload'] / $mb);
        $ping = (float)sprintf("%0.3f", $results['ping_avg']);

        # Store values to return later
        $r_value['download'][$key][$i] = $download;
        $r_value['upload'][$key][$i] = $upload;
        $r_value['ping'][$key][$i] = $ping;

      }else{

        # Store nothing the no results where found
        $r_value['download'][$key][$i] = 0;
        $r_value['upload'][$key][$i] = 0;
        $r_value['ping'][$key][$i] = 0;

      }
    }
  }

  $db->close();
  return $r_value;

}

$db_location = "/srv/databases/sst/results.db";
$result_list = get_all_test_results($db_location);

echo json_encode($result_list);

?>
