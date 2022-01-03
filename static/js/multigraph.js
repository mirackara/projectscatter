var graphList = [];
var chartContainerList = [];


//  Handles if enter was clicked on search bar
var input = document.getElementById("searchBar");
input.addEventListener("keyup", function(event) {
  if (event.keyCode === 13) {
  event.preventDefault();
  document.getElementById("clickMe").click();
  }
});

// Changes from List View/Grid View
function viewChange(viewPreference) {
  if(viewPreference == "listView"){
    for(var i = 0; i < graphList.length; ++i){
      graphList[i].options.width = 1200;
      graphList[i].render();
      var currChartID = String(chartContainerList[i]);
      document.getElementById(currChartID).className = "col-md-12";
    }
    localStorage['viewPref'] = "listView";
  }else{
    for(var i = 0; i < graphList.length; ++i){
      graphList[i].options.width = 600;
      graphList[i].render();
      var currChartID = String(chartContainerList[i]);
      document.getElementById(currChartID).className = "col-md-6";
    }
    localStorage['viewPref'] = "gridView";

  }
}


function searchCompare() {
    document.getElementById("showsToCompare").value = showListFull;
  }

function loadChart(chartName,currShowName, tempData){
    var chartData = new Object();
    chartData.title = {text:currShowName};
    chartData.axisY = {title: "Rating", gridThickness: 0, maximum: 10.3};
    chartData.axisX = {
        title: "Episode", gridThickness: 0,
        labelFormatter: function () {
            return " ";
        },
    };
    chartData.toolTip = true;
    chartData.visible = true;
    chartData.showInLegend = true;
    chartData.yValueFormatString = "##.0";
    chartData.data = tempData.data;
    chart = new CanvasJS.Chart(chartName, {
        theme:"dark2",
        title: chartData.title,
        width: 1200,
        axisY: chartData.axisY,
        axisX : chartData.axisX,
        animationEnabled: true,
        data : chartData.data,
        yValueFormatString : chartData.yValueFormatString,
        showInLegend : chartData.showInLegend,
        legend:{
            cursor:"pointer",
            itemclick : function(e){
                if (typeof(e.dataSeries.visible) == undefined || e.dataSeries.visible ){
                    e.dataSeries.visible = false;
                  } else {
                    e.dataSeries.visible = true;
                  }
                  chart.render();
              }
          }
          });
      chart.render(chart.data, chart.options);
      graphList.push(chart);
      graphSize++;

}
function del(currChart){ // Remove show from list
  // If theres only 1 graph left, clear screen
  if (graphSize == 1){
    graphSize = 0;
    clearAll();
    return;
  }
  var graphDiv = currChart.id;
  var itemToDelete = graphDiv[graphDiv.length - 1];
  graphSize--;
  var deleteGraph = graphDiv + 'col';
  // Add show to showsToRemove, this will be passed onto Python in the request
  document.getElementById("showsToRemove").value += showListFull[itemToDelete] + ",";
  document.getElementById(deleteGraph).style.display = "none";
}

function clearAll(){
  // First, we empty cookie
  localStorage.clear();
  // Then, we send the removeAll command to Python
  document.getElementById("showsToRemove").value += "REMOVEALL";
}


for (i = 0; i <= numOfShows; ++i) {
    // Converting Raw Show Data from Python
    var currChart = "chartContainer" + i; // Create a new chartContainer for each show
    if (showData[i] == undefined) {
        continue;
    }
    var currShowData = Object.values(showData[i])[0]; // Seasons Data
    var currShowName = Object.keys(showData[i])[0];  // Show Name
    var dataToPush = new Object();
    var currEpGraph = 0;
    dataToPush.data = [];
    var epCounter = 0;
    // Typically, Double nested for loops wouldn't be too great for performance.
    // However, Considering a TV Show has a small number of episodes
    // Complexity wouldn't be an issue.

    // "Unpacking" Raw Episode Data from Python.
    for (j = 1; j < currShowData.length; ++j) {
        var fullShowData = new Object();
        fullShowData.dataPoints = [];
        var seasonData = Object.values(currShowData[j]);
        fullShowData.name = "Season " + j;
        fullShowData.showInLegend = true;
        fullShowData.showLine = "true";
        fullShowData.type = "spline";
        fullShowData.visible = true;
        fullShowData.yValueFormatString = "##.0";
        for (k = 0; k < seasonData[0].length; ++k) {
            // J = current Season
            // seasonData[0][k][0] = Episode Name
            // seasonData[0][k][1] = Episode Rating
            var currEp = k + 1
            epCounter++;
            var EpName = seasonData[0][k][1];
            // FIX : Names not showing up in graph
            fullShowData.dataPoints.push({
                legendText: EpName,
                label: "Ep. " + currEp + " Season " + j,
                x: epCounter,
                y: parseFloat(seasonData[0][k][1]),
                fill: false
            });
            currEpGraph++;
        }
        dataToPush.data.push(fullShowData);
    }
    $("#container").append('<div class = "col-md-12" id="' + currChart + 'col"><div id="' + currChart + '" style="height: 600px; max-width: 1200px; margin: 0px auto;"></div> <input id=' + currChart + '-btn' + ' type="button" width = 100% value= "clear" onclick = "del(' + currChart + ');" class="btn btn-primary"/>');
    loadChart(currChart, currShowName, dataToPush);
}
window.onload = function checkView() {
    console.log(statusCode);
    if (statusCode == 200) { // Successfully loaded data from Python
        console.log("Pass");
        return;
    } else if (statusCode == 400) { // Did not load data from Python
        console.log("fail!");
        document.getElementById("queryResponse").innerHTML = "Cannot find show. Try another one.";
    } else if (statusCode == 404) { // Did not load data from Python
        console.log("fail! Loading Default Show");
        document.getElementById("queryResponse").innerHTML = "Cannot find show. Try another one.";
        chart = loadChartData();
        // calculateTrendLine(chart);
        chart.render();
    } else if (statusCode == 401) {
        console.log("failed mulitple shows");
        // Make a container element for the list
        listContainer = document.createElement('div'),
            // Make the list
            listElement = document.createElement('ul'),
            // Set up a loop that goes through the items in listItems one at a time
            numberOfListItems = showNamesMultiple.length - 1;

        // Add it to the page
        document.getElementById('menuBar').appendChild(listContainer);
        listContainer.appendChild(listElement);
        for (var i = 0; i < numberOfListItems; ++i) {
            // create an item for each one
            var listItem = document.createElement('input');
            listItem.type = "button";
            // Add the item text
            listItem.value = showNamesMultiple[i];
            listItem.addEventListener('click', function () {
                showChosen(this.value);
            });
            // Add listItem to the listElement
            listElement.appendChild(listItem);
            console.log(listItem);
        }
    }

    function showChosen(show) {
        document.getElementById("showsToRemove").value += showNamesMultiple[showNamesMultiple.length - 1] + ",";
        showListFull += show;
        document.getElementById('searchBar').value = String(show);
        searchCompare();
        document.getElementById('compareBtn').click()
    }
}
