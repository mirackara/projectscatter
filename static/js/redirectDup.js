
//  Handles if enter was clicked on search bar
var input = document.getElementById("searchBar");
input.addEventListener("keyup", function(event) {
  if (event.keyCode === 13) {
  event.preventDefault();
  document.getElementById("clickMe").click();
  }
});

function printData() {
  var chartData = new Object();
  chartData.theme = "dark2";
  chartData.animationEnabled = true;
  chartData.title = {text:spliced};
  chartData.axisY = {title: "Rating", gridThickness: 0 };
  chartData.axisX = {title: "Episode", gridThickness: 0,     labelFormatter: function(){
    return " ";
  }};
  chartData.toolTip = {shared: "false"};
  chartData.data = [];
  var i = 1;
  var testCounter = 0;
  for (i = 1; i <= seasons; ++i) {
    console.log(i);
    var seasonName = "Season " + i;
    var currSeason = showData[spliced][i];
    var j = 1;
    var tempData = new Object();
    tempData.type = "spline";
    tempData.visible = true;
    tempData.showInLegend = true;
    tempData.yValueFormatString = "##.0";
    tempData.name = seasonName;
    tempData.dataPoints = [];
    for (j = 1; j < currSeason[seasonName].length; ++j){
      var epData = [];
//      console.log(currSeason[seasonName][j][0]); // Ep Name
//      console.log(currSeason[seasonName][j][1]); // Ep Rating
      tempData.dataPoints.push({name: [i] + " " + currSeason[seasonName][j][0] ,  label: "Ep. " + j + " Season " + [i], x:testCounter , y: parseFloat(currSeason[seasonName][j][1]), fill : false});
      tempData.showLine = "true";
      testCounter++;
    }

    chartData.data.push(tempData);
    console.log(chartData.data);
  }
  return chartData;
}
function checkBox() {
  var checkBox = document.getElementById("yAxisScale");
      if (checkBox.checked == true){
    console.log("Check True!");
    loadChartData(true);
    } else {
    console.log("Check False!");
    loadChartData(false);
  }
}

function toggleDataSeries(e) {
  if (typeof(e.dataSeries.visible) === "undefined" || e.dataSeries.visible ){
    e.dataSeries.visible = false;
  } else {
    e.dataSeries.visible = true;
  }
  chart.render();
}

function loadChartData(isScaled){
  chartData = printData();
  if (isScaled){
    console.log("Scaled!");
    // chartData.options = {scales: {yAxes :  {ticks: {min: 0}}}};
  } else{
    console.log("Not Scaled!");
    chartData.options = {scales: {yAxes : {beginAtZero : false}}};
  }
  chart = new CanvasJS.Chart("chartContainer", {
    theme:chartData.theme,
    animationEnabled: chartData.animationEnabled,
    title:chartData.title,
    axisY :chartData.axisY,
    axisX : chartData.axisX,
    toolTip: chartData.toolTip,
    legend:{
      cursor:"pointer",
      itemclick : toggleDataSeries
    },
    data: chartData.data
      });
  return chart;
}

function search() {
  var showSearch = document.getElementById('searchBar').value; // First element
  if (showSearch.length == 0){  // Empty Search Bar
    console.log("Empty!")
    document.getElementById("showNameID").innerHTML = "Please type a Show Name";
  } else { // Redirect to search
    var redirect = "http://127.0.0.1:5000/search/"; 
    var redirectURL = redirect.concat(showSearch);
    console.log(showSearch)
    location.replace(redirectURL);
    return ` You searched for ${showSearch}`;
  }
}
//- Using a function pointer:
document.getElementById("clickMe").onclick = search;
window.onload = function checkFlaskStatus() {
  if (statusCode == 200) { // Successfully loaded data from Flask
    console.log("Pass");
    try {
      spliced = showName.match(/&#39;([^']+)&#39;/)[1];
    }
    catch {
      spliced = showName.match(/&#34;([^']+)&#34;/)[1]; // Show name cleaned up
    }
    spliced = decodeURIComponent(escape(spliced));
    spliced = spliced.replace("&#39;", "'"); // Replace UTF8 code for ' with an actual '

//    document.getElementById("showNameID").innerHTML = decodeURIComponent(escape(spliced)); // Set Series Name in HTML
    chart = loadChartData();
    var options= {
      scales:{
          yAxes: [{
              min: 0 //this will remove all the x-axis grid lines
          }]
      }
  };
    chart.render();
    

    
    return;
  }
  if (statusCode == 500) {  // Inital Load
    console.log("Load");
    return;
  }
  if (statusCode = 400) { // Did not load data from Flask
    console.log("fail!");
    document.getElementById("showNameID").innerHTML = "Cannot find show. Try another one.";
  }
}