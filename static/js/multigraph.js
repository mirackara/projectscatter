

function loadChart(chartName,currShowName, tempData){
    var chartData = new Object();
    chartData.title = {text:currShowName};
    chartData.axisY = {title: "Rating", gridThickness: 0, maximum : 10.3};
    chartData.axisX = {title: "Episode", gridThickness: 0,     
                       labelFormatter: function(){
                                          return " ";
                                      },
                      };  
    chartData.toolTip = {shared: "false"};
    chartData.visible = true;
    chartData.showInLegend = true;
    chartData.yValueFormatString = "##.0";
    chartData.data = tempData
    chart = new CanvasJS.Chart(chartName, {
        theme:"dark2",
        title: chartData.title,
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
    
}

for (i = 0; i <= numOfShows; ++i) {
    // Converting Raw Show Data from Python
    var currChart = "chartContainer" + i; // Create a new chartContainer for each show
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
        for (k = 0; k < seasonData[0].length; ++k){
            // J = current Season
            // seasonData[0][k][0] = Episode Name
            // seasonData[0][k][1] = Episode Rating
            var currEp = k + 1
            fullShowData.dataPoints.push({label: "Ep. " + currEp + " Season " + j, 
                                          x: currEpGraph,
                                          y: parseFloat(seasonData[0][k][1]),
                                          name: seasonData[0][k][0],
                                          fill : false
                                        });
            currEpGraph++;
        }
        fullShowData.name = "Season " + j;
        fullShowData.showInLegend = true;
        fullShowData.showLine = true;
        fullShowData.type = "spline";
        fullShowData.visible = true;
        fullShowData.yValueFormatString = "##.0";
        dataToPush.data.push(fullShowData);
    }
    // console.log(dataToPush);
    $("#container").append(' <br> <div id="' + currChart +  '" style="height: 600px; max-width: 1200px; margin: 0px auto;"></div>');
    

    loadChart(currChart,currShowName, dataToPush.data);
}

console.log("test");



