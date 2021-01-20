
// Helps format data sets
function build_data_set(data_key, data_sets){

  // Add hourly title
  var hour_labels = [];
  for(var i = 1; i < 25; ++i)
    hour_labels.push(i.toString());

  // create data sets with styles for chart.js
  var return_data = {
    labels: hour_labels,
    datasets: [{
      label:'Today',
      data: data_sets[data_key]['today'],
      borderColor: 'rgb(255, 0, 0)',
      pointBackgroundColor: 'rgb(255, 0, 0)',
      borderWidth: 2,
      fill: false,
      lineTension:"0.1"
    },{
      label:'Life Time',
      data:data_sets[data_key]['life'],
      borderColor: 'rgb(0, 255, 0)',
      pointBackgroundColor: 'rgb(0, 255, 0)',
      borderWidth: 2,
      fill: false,
      lineTension:"0.1"
    },{
      label:'Yeasterday',
      hidden:true,
      data:data_sets[data_key]['yeasterday'],
      borderColor: 'rgb(204, 204, 0)',
      pointBackgroundColor: 'rgb(204, 204, 0)',
      borderWidth: 2,
      fill: false,
      lineTension:"0.1"
    }]
  };

  return return_data;
}


// Pull each chart out of charts and draw it now
function draw_all_charts(charts, data_set){
  charts.forEach(chart =>{
    draw_chart(chart, data_set);
  });
}

// Build the chart to be presented
function draw_chart(chart, data_set){

  // Use link provided from html to draw on canvas
  var ctx = document.getElementById(chart['link']);

  // Set up the chart
  var myChart = new Chart(ctx, {

    type: 'line',

    // Use chart key to extract data from json object
    data: build_data_set(chart['key'], data_set),
    options:{
      title:{
        display:true,text: chart['title'],fontSize:18
      },
      legend:{
        labels:{
          usePointStyle: true,
          fontSize:10
        }
      }
    }
  });
}

// Fetch data from php server side
function fetch_data(charts, url){

  // execute following async after request is sent
  var xmlhttp = new XMLHttpRequest();
  xmlhttp.onreadystatechange = function(){
    if (this.readyState == 4 && this.status == 200){
      var tmp = this.responseText;
      var json_obj = JSON.parse(tmp);
  
      // build the chart based on id and data from server
      draw_all_charts(charts, json_obj);
    }
  };

  // Set request async
  xmlhttp.open("GET", url, true);
  xmlhttp.send();

}

function load_all_charts(download, upload, ping){

  var charts = [{link:download,key:'download',title:'Download Speeds'},
                {link:upload,key:'upload',title:'Upload Speeds'},
                {link:ping,key:'ping',title:'Ping Speeds'}];

  // Fetch data from this url
  var url = "http://192.168.1.49/sst/php/get_speeds.php";
  fetch_data(charts, url);

}
