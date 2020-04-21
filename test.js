<script src="d3.min.js?v=3.2.8"></script>

<script type="text/javascript"charset="utf-8">
    d3.text("data.csv", function(data) {
        var parsedCSV = d3.csv.parseRows(data);

        var container = d3.select("body")
            .append("table")

            .selectAll("tr")
                .data(parsedCSV).enter()
                .append("tr")

            .selectAll("td")
                .data(function(d) { return d; }).enter()
                .append("td")
                .text(function(d) { return d; });
    });
</script>
