var graphList = [];
var chartContainerList = [];

console.log(graphList);
console.log(chartContainerList);

window.onload = function checkView() {
  console.log(localStorage['viewPref']);
  if (localStorage['viewPref'] != ""){
    viewChange(localStorage['viewPref']);
  }
}


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
    var showSearch = document.getElementById('searchBar').value; // First element
    if (showSearch.length == 0){  // Empty Search Bar
      console.log("Empty!")
      document.getElementById("showNameID").innerHTML = "Please type a Show Name";
    } else { // Redirect to search
      var myVar = localStorage['myKey'] || "";
      var tmpArr = myVar.split('+');

      if (!lastShowAdded){ // If the last show was not found, remove it from cookie
        //  Find all occurances of '+' in myVar.
        var indices = [];
        for(var i=0; i<myVar.length;i++) {
            if (myVar[i] === "+") indices.push(i);
        }
        var showToRemove = myVar.substring((indices[indices.length-1],indices[indices.length-2]));
        myVar = myVar.replace(showToRemove, '+');
      }
      localStorage['myKey'] = myVar + showSearch +  '+'; // Store cookie of all searches thus far
    
      var redirect = "http://www.scattertv.com/compare/";
      var redirectURL = redirect.concat(myVar + showSearch +  '+');
      location.replace(redirectURL);
    }
  }

function loadChart(chartName,currShowName, tempData){
    var chartData = new Object();
    chartData.title = {text:currShowName};
    chartData.axisY = {title: "Rating", gridThickness: 0, maximum : 10.3};
    chartData.axisX = {title: "Episode", gridThickness: 0,     
                       labelFormatter: function(){
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
                if (typeof(e.dataSeries.visible) === "undefined" || e.dataSeries.visible ){
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
  var myVar = localStorage['myKey'];
  var tmpArr = myVar.split('+');

  // tmpArr[itemToDelete] Show to delete
  tmpArr.splice(itemToDelete, 1);
  if (tmpArr.length == 0){ // If there aren't any shows to clear, empty storage
    localStorage.clear();
  }

  var cookieToPush;
  for (var i = 0; i < tmpArr.length; ++i){
    if (tmpArr[i] == undefined || tmpArr[i] == ""){
      continue;
    } else {
      if (i == tmpArr.length-1 ){
        cookieToPush += tmpArr[i];
      }else { 
        cookieToPush += tmpArr[i] + '+';
      }
    }
  }
  if (cookieToPush == undefined){
    graphSize--;
    var deleteGraph = graphDiv + 'col';
    document.getElementById(deleteGraph).style.display = "none"; // Hides graph
    return;
  } else{
      var cleanedCookie = cookieToPush.replace('undefined','');
      console.log(cleanedCookie);
  
      localStorage['myKey'] = cleanedCookie; // only strings
  }
  graphSize--;
  var deleteGraph = graphDiv + 'col';
  document.getElementById(deleteGraph).style.display = "none";  
}

function clearAll(){
  // First, we empty cookie
  localStorage.clear();

  // Next, we clear the URL
  var redirect = "http://www.scattertv.com/";
  location.replace(redirect);
}


for (i = 0; i <= numOfShows; ++i) {
    // Converting Raw Show Data from Python
    var currChart = "chartContainer" + i; // Create a new chartContainer for each show
    if (showData[i] == undefined){
      continue;
    }
    var currShowData = Object.values(showData[i])[0]; // Seasons Data
    var currShowName = Object.keys(showData[i])[0];  // Show Name
    var dataToPush = new Object();
    var currEpGraph = 0;
    dataToPush.data = [];
    // Typically, Double nested for loops wouldn't be too great for performance. 
    // However, Considering a TV Show has a small number of episodes
    // Complexity wouldn't be an issue.

    // "Unpacking" Raw Episode Data from Python.
    for (j = 1; j < currShowData.length; ++j){
        var fullShowData = new Object();
        fullShowData.dataPoints = [];
        var seasonData = Object.values(currShowData[j]);
        fullShowData.name = "Season " + j;
        fullShowData.showInLegend = true;
        fullShowData.showLine = "true";
        fullShowData.type = "spline";
        fullShowData.visible = true;
        fullShowData.yValueFormatString = "##.0";
        for (k = 0; k < seasonData[0].length; ++k){
            // J = current Season
            // seasonData[0][k][0] = Episode Name
            // seasonData[0][k][1] = Episode Rating
            var currEp = k + 1
            var EpName = seasonData[0][k][0];
            // FIX : Names not showing up in graph
            fullShowData.dataPoints.push({legendText: EpName , label: "Ep. " + currEp + " Season " + j,  x: currEpGraph, y: parseFloat(seasonData[0][k][1]), fill : false }); 
            
          //  console.log(seasonData[0][k][0]);
            currEpGraph++;
        }
        
        dataToPush.data.push(fullShowData);
    }
    chartContainerList.push(currChart+"col");
    $("#container").append('<div class = "col-md-12" id="' + currChart +  'col"><div id="' + currChart +  '" style="height: 600px; width: 100%;"></div> <input id='+ currChart + '-btn' + ' type="button" width = 100% value= "clear" onclick = "del('+ currChart + ');" class="btn btn-primary"/>');
    loadChart(currChart,currShowName, dataToPush);
  }


