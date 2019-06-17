// defining $ symbol
/*global $*/

// Initial data to set up graph
let data = [];

$('#summarySelect').change(function(){
    var dropdown = this.value;
    $.getJSON("/summary/data", function(jsonData){
    
    if(dropdown=="opt1") {
        var Trans = jsonData[1];
        data = [
            { group: "Automatic", value: Trans.Auto, value2: Trans.AutoN },
            { group: "Manual", value: Trans.Manual, value2: Trans.ManualN },
            { group: "SemiAuto", value: Trans.SemiAuto, value2: Trans.SemiAutoN },
            { group: "Sequential", value: Trans.Sequential, value2: Trans.SequentialN }
        ];
        update(data);
    }
    if(dropdown=="opt2") {
        var Accel = jsonData[2];
        data = [
            { group: "Less than 4 seconds", value: Accel.LT4, value2: Accel.LT4N },
            { group: "Less than 7 seconds", value: Accel.LT7, value2: Accel.LT7N },
            { group: "More than 7 seconds", value: Accel.MT7, value2: Accel.MT7N }
        ];
        update(data);
    }
    if(dropdown=="opt3") {
        var Region = jsonData[0];
        data = [
            { group: "USDM", value: Region.USDM, value2: Region.USDMN },
            { group: "JDM", value: Region.JDM, value2: Region.JDMN },
            { group: "Euro", value: Region.Euro, value2: Region.EuroN }
        ];
        update(data);
        }
 });
});

 // set the dimensions and margins of the graph
 var margin = { top: 30, right: 30, bottom: 70, left: 60 },
     width = 460 - margin.left - margin.right,
     height = 400 - margin.top - margin.bottom;

 // append the svg object to the body of the page
 var svg = d3.select("#my_dataviz")
  .append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
  .append("g")
  .attr("transform",
   "translate(" + margin.left + "," + margin.top + ")");
   
 var Tooltip = d3.select("#my_dataviz")
    .append("div")
    .style("opacity", 0)
    .attr("class", "tooltip")
    .style("background-color", "white")
    .style("border", "solid")
    .style("border-width", "2px")
    .style("border-radius", "5px")
    .style("padding", "5px");  
 
 var mouseover = function(d) {
    Tooltip
      .style("opacity", 1);
    d3.select(this)
      .style("stroke", "black")
      .style("opacity", 1);
  };
  var mousemove = function(d) {
    Tooltip
      .html("Cars that are " + d.group + ": " + d.value)
      .style("left", (d3.mouse(this)[0]+70) + "px")
      .style("top", (d3.mouse(this)[1]) + "px")
  };
  var mouseleave = function(d) {
    Tooltip
      .style("opacity", 0);
    d3.select(this)
      .style("stroke", "none")
      .style("opacity", 0.8);
  };
 
 // Initialize the X axis
 var x = d3.scaleBand()
     .range([0, width])
     .padding(0.2);
 var xAxis = svg.append("g")
     .attr("transform", "translate(0," + height + ")");

 // Initialize the Y axis
 var y = d3.scaleLinear()
     .range([height, 0]);
 var yAxis = svg.append("g")
     .attr("class", "myYaxis");

function update(data) {
     // Update the X axis
     x.domain(data.map(function(d) { return d.group; }));
     xAxis.call(d3.axisBottom(x));

     // Update the Y axis
     y.domain([0, d3.max(data, function(d) { return d.value })]);
     yAxis.transition().duration(1000).call(d3.axisLeft(y));

     // Create the u variable
     var u = svg.selectAll("rect")
         .data(data);
         
     u
         .enter()
         .append("rect") // Add a new rect for each new elements
         .on("mouseover", mouseover)
         .on("mousemove", mousemove)
         .on("mouseleave", mouseleave)
         .merge(u) // get the already existing elements as well
         .transition() // and apply changes to all of them
         .duration(1000)
         .attr("x", function(d) { return x(d.group); })
         .attr("y", function(d) { return y(d.value); })
         .attr("width", x.bandwidth())
         .attr("height", function(d) { return height - y(d.value); })
         .attr("fill", "#448aff");
     
     // If less group in the new dataset, it delete the ones not in use anymore
     u
         .exit()
         .remove();
    table(data);
}

function table(data) {
    
    var summaryTable = $('<table></table>');
    for(var i=0; i < data.length; i++) {
        var tr = $('<tr></tr>');
        for(var key in data[i]) {
            var td = $('<td></td>');
            td.attr('class', key);
            td.text(data[i][key]);
            tr.append(td);
        }
    summaryTable.append(tr);
    }
    
    var divContainer = document.getElementById("tableDiv");
    divContainer.innerHTML = "";
    divContainer.append(summaryTable[0]);
}