//  Handles if enter was clicked on search bar
var input = document.getElementById("searchBar");
input.addEventListener("keyup", function(event) {
  if (event.keyCode === 13) {
  event.preventDefault();
  document.getElementById("search").click();
  }
});
//  console.log(showData);
//  EXPERIMENTAL : Trendlines
function calculateTrendLine(chart){
  var a, b, c, d, e, slope, yIntercept;
  for (var i = 0; i <= seasons; ++i ){
    var xSum = 0, ySum = 0, xySum = 0, xSquare = 0, dpsLength = chart.data[i].dataPoints.length;
    for(var j = 0; j < dpsLength; j++)
        xySum += (chart.data[i].dataPoints[j].x * chart.data[i].dataPoints[j].y)
    a = xySum * dpsLength;

    for(var k = 0; k < dpsLength; k++){
        xSum += chart.data[i].dataPoints[k].x;
        ySum += chart.data[i].dataPoints[k].y;
    }
    b = xSum * ySum;

    for(var z = 0; z < dpsLength; z++)
        xSquare += Math.pow(chart.data[i].dataPoints[z].x, 2);
    c = dpsLength * xSquare;

    d = Math.pow(xSum, 2);
    slope = (a-b)/(c-d);
    e = slope * xSum;
    yIntercept = (ySum - e) / dpsLength;

    var startPoint = getTrendLinePoint(chart.data[i].dataPoints[i].x, slope, yIntercept);
    var endPoint = getTrendLinePoint(chart.data[i].dataPoints[dpsLength-1].x, slope, yIntercept);

    chart.addTo("data",{
        type: "line", //Line series showing trend
        markerSize: 0,
        dataPoints: [startPoint, endPoint]
    });
  }
}
function getTrendLinePoint(x, slope, intercept){
  return {x: x, y: ((slope * x) + intercept)};
}
function printData() {
  var chartData = new Object();
  chartData.theme = "dark2";
  chartData.animationEnabled = true;
  console.log(showName);
  chartData.title = {text:showName};
  chartData.axisY = {title: "Rating", gridThickness: 0, maximum : 10.3};
  chartData.axisX = {title: "Episode", gridThickness: 0,
                     labelFormatter: function(){
                                        return " ";
                                    },
                    };
  chartData.toolTip = {shared: "false"};
  chartData.data = [];
  var i = 1;
  var testCounter = 0;
  for (i = 1; i <= seasons; ++i) {
    console.log(i);
    var seasonName = "Season " + i;
    var currSeason = showData[showName][i];
    var j = 1;
    var tempData = new Object();
    tempData.type = "spline";
    tempData.visible = true;
    tempData.showInLegend = true;
    tempData.yValueFormatString = "##.0";
    tempData.name = seasonName;
    tempData.dataPoints = [];
    for (j = 0; j < currSeason[seasonName].length; ++j){
      var epData = [];
      var epNum = j + 1
      //  console.log(currSeason[seasonName][j][0]); // Ep Name
      //  console.log(currSeason[seasonName][j][1]); // Ep Rating
      tempData.dataPoints.push({name: currSeason[seasonName][j][0] ,  label: "Ep. " + epNum + " Season " + [i], x:testCounter , y: parseFloat(currSeason[seasonName][j][1]), fill : false});
      tempData.showLine = "true";
      testCounter++;
    }
    chartData.data.push(tempData);
    // console.log(chartData.data);
  }
  return chartData;
}
function checkBoxScaler(isScaled) {
      if (isScaled){
          loadChartData(true);
    } else {
    loadChartData(false);
  }
}
function compareRedirect(){
    var input = document.getElementById("searchBar").value;
    var concatTitles = [input, showName];
    document.getElementById("searchBar").innerHTML = String(concatTitles);
    document.getElementById("showsToCompare").value = concatTitles
}
function buttonChecked() {
    $(function() {
      $('#checkBtn').click(function() {
          $(':checkbox').prop('checked', !$(':checkbox').prop('checked'));
      });
  });
  checkBoxScaler(); // Scaler Function
}
function toggleDataSeries(e) {
  if (typeof(e.dataSeries.visible) === "undefined" || e.dataSeries.visible ){
    e.dataSeries.visible = false;
    chart.render();
  } else {
    e.dataSeries.visible = true;
  }
  chart.render();
}

function loadChartData(isScaled){
  chartData = printData();
  if (isScaled){
    console.log("Scaled!");
    chartData.axisY = {title: "Rating", gridThickness: 0, minimum: 0, maximum: 10};
  } else{
    console.log("Not Scaled!");
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
  chart.render(chart.data, chart.options);
  return chart;
}
function bestEpisode(data) {
  for (i = 1; i <= seasons; ++i) {
    for (j = 1; j < showData[seasonName].length; ++j){
      return showData[seasonName][j][1];
    }
  }
}
function search(wantsCompare) {
    if (wantsCompare == "compare") {
        localStorage['myKey'] = spliced + '+';
        lastShowAdded = "true";
        searchCompare();
        return;
    }
    var showSearch = document.getElementById('searchBar').value; // First element
    console.log(showSearch);

    if (showSearch.length == 0) {  // Empty Search Bar
        console.log("Empty!")
        document.getElementById("showNameID").innerHTML = "Please type a Show Name";
    }
}
window.onload = function checkStatus() {
  if (statusCode == 200) { // Successfully loaded data from Python
    console.log("Pass");
    chart = loadChartData();
    // calculateTrendLine(chart);
    chart.render();
    document.getElementById("bestEp").innerHTML = bestEpisode(chart.data);
    return;
  }
  if (statusCode == 500) {  // Inital Load
    console.log("Load");
    return;
  }
  if (statusCode = 400) { // Did not load data from Python
      console.log("fail!");
      chart = loadChartData();
      // calculateTrendLine(chart);
      chart.render();
      document.getElementById("bestEp").innerHTML = bestEpisode(chart.data);
      document.getElementById("worstEp").innerHTML = bestEpisode(chart.data);
      document.getElementById("showNameID").innerHTML = "Cannot find show. Try another one.";


  }
}

