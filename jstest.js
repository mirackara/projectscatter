
var data;
  $.ajax({
    type: "GET",  
    url: "CommunityData.csv",
    dataType: "text",       
    success: function(response)  
    {
    data = $.csv.toArrays(response);
    generateHtmlTable(data);
    }   
  });
    


