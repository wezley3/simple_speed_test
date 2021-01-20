<?php

function get_todays_all($db_location){

  $mb = 1048576;

  # Create a dictionary to store results
  $r_value = array();
  $keys = ['download', 'upload', 'ping'];

  foreach($keys as $key){
    $r_value[$key] = array();
    $r_value[$key]['today'] = array();
    $r_value[$key]['yeasterday'] = array();
    $r_value[$key]['life'] = array();
  }


  $day_query_template = "select download, upload, ping_avg from results where strftime('%s', ins_date) = '%s' and strftime('%s', ins_date) = '%s';";

  $life_query_template = "select avg(download) as download, avg(upload) as upload, avg(ping_avg) as ping_avg from results where strftime('%s', ins_date) = '%s';";

  $db = new SQLite3($db_location);

  for($i = 0; $i < 24; ++$i){

    if($i < 10)
      $ins_date = sprintf('0%d', $i);
    else
      $ins_date = sprintf('%d', $i);


    # Fetch todays data
    $today_query = sprintf($day_query_template, "%H", $ins_date, "%d", date('d'));
    $yeasterday_query = sprintf($day_query_template, "%H", $ins_date, "%d", date('d') - 1);


    $results = $db->query($today_query)->fetchArray();

    if($results != NULL){
      $r_value['download']['today'][$i] = $results['download'] / $mb;
      $r_value['upload']['today'][$i] = $results['upload'] / $mb;
      $r_value['ping']['today'][$i] = $results['ping_avg'];
    }else{
      $r_value['download']['today'][$i] = 0;
      $r_value['upload']['today'][$i] = 0;
      $r_value['ping']['today'][$i] = 0;
    }
      
    $results = $db->query($yeasterday_query)->fetchArray();

    if($results != NULL){
      $r_value['download']['yeasterday'][$i] = $results['download'] / $mb;
      $r_value['upload']['yeasterday'][$i] = $results['upload'] / $mb;
      $r_value['ping']['yeasterday'][$i] = $results['ping_avg'];
    }else{
      $r_value['download']['yeasterday'][$i] = 0;
      $r_value['upload']['yeasterday'][$i] = 0;
      $r_value['ping']['yeasterday'][$i] = 0;
    }


    $life_query = sprintf($life_query_template, "%H", $ins_date);
    $results = $db->query($life_query)->fetchArray();

    if($results != NULL){
      $r_value['download']['life'][$i] = $results['download'] / $mb;
      $r_value['upload']['life'][$i] = $results['upload'] / $mb;
      $r_value['ping']['life'][$i] = $results['ping_avg'];
    }else{
      $r_value['download']['life'][$i] = 0;
      $r_value['upload']['life'][$i] = 0;
      $r_value['ping']['life'][$i] = 0;
    }


  }


  $db->close();

  return $r_value;

}


$username = posix_getpwuid(posix_geteuid())['name'];
$result_list = get_todays_all("/home/wez/databases/speed_tests.db");

echo json_encode($result_list);

?>
