//Add the selector
var options_holder = [2011, 2012, 2013, 2014, 2015];

var select = d3.select('body')
.select("#selector")
.append('select')
.attr('id','inds')
.on('change',onchange)

var options = select
.selectAll('option')
.data(options_holder).enter()
.append('option')
.attr('selected',function(d){if(d==2011){return "selected";}})
.attr('value',function(d){return d;})
.text(function (d) { return d; })

//Define basic parameters
var margin = {top: 50, right: 20, bottom: 100, left: 200},
width = 960 - margin.right - margin.left,
height = 800 - margin.top - margin.bottom;

var itemSize = 90,
cellSize = itemSize - 1;

var data=[]
var colors =["#fff7f3","#fde0dd","#fcc5c0","#fa9fb5","#f768a1","#dd3497","#ae017e","#7a0177","#49006a"]
 
function heatmap(select_area,which_year){
  var data=[]
  //Load the data
  d3.csv('heatmap.csv').then(function (response) {
    var filtered = response.filter(function (d){
      if (+d["Year"] == which_year) {return d}
    })
    filtered.forEach(function(d){
      for (var key in d){
        var obj = {};
        if(key != "Crime Type" && key!= "Year"){
          obj.borough = key;
          obj.count = +d[key];
          obj.crime_type = d["Crime Type"];
          data.push(obj)
        }
      }
    })

   //Create svg
    var svg = d3.select(select_area)
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var x_elements = d3.set(data.map(function( item ) { return item.crime_type; } )).values().sort(d3.ascending),
    y_elements = d3.set(data.map(function( item ) { return item.borough; } )).values().sort(d3.ascending);

    //Define the scale for x, y, color
    var xScale = d3.scaleBand()
    .domain(x_elements)
    .rangeRound([0, x_elements.length * itemSize]);

    var yScale = d3.scaleBand()
    .domain(y_elements)
    .rangeRound([0, y_elements.length * itemSize]);

    var colorScale = d3.scaleQuantile()
    .domain([0,9, d3.max(data, function (d) { return d.count; })])
    .range(colors);

    //Create X axis and y axis
    var xAxis = d3.axisTop(xScale)
    .tickFormat(function (d) {return d;})

    var yAxis = d3.axisLeft(yScale)
    .tickFormat(function (d) {return d;})

    //Create cells
    var cells = svg.selectAll('rect')
    .data(data)
    .enter()
    .append('g')
    .append('rect')
    .attr('class', 'cell')
    .attr("rx", 8)
    .attr("ry", 8)
    .attr('width', cellSize)
    .attr('height', cellSize)
    .attr('y', function(d) { return yScale(d.borough); })
    .attr('x', function(d) { return xScale(d.crime_type); })
    .attr('fill', function(d) { return colorScale(d.count); });

    //Add x axis
    svg.append("g")
    .attr("class", "x axis")
    .call(xAxis)
    .selectAll('text')
    .attr('font-weight', 'normal')
    .style("text-anchor", "start")
    .attr("dy", "3em")
    .attr('transform', 'translate('+(-itemSize/4)+',' + (height-margin.top-margin.bottom*1.6) + ')');

    //Add y axis
    svg.append("g")
    .attr("class", "y axis")
    .call(yAxis)
    .selectAll('text')
    .attr('font-weight', 'normal');

    //add y axis label
    svg.append("text")
    .attr("transform","rotate(-90)")
    .attr("y",0-margin.left*0.7)
    .attr("x",-(height*0.35))
    .attr("dy","1em")
    .style("text-anchor","middle")
    .style("font-size","22px")
    .text("Borough");

    //add x axis label
    svg.append("text")
    .attr("transform", "translate("+(width*0.37)+","+(height-margin.top-margin.bottom*0.7)+")")
    .style("text-anchor","middle")
    .style("font-size","22px")
    .text("Crime Type");

    //add legend label
    svg.append("text")
    .attr("transform", "translate("+(-20)+","+(height-65)+")")
    .style("text-anchor","end")
    .style("font-size","18px")
    .text("No. of Crimes");

    //add legend
    var legend = svg.selectAll(".legend")
    .data([0].concat(colorScale.quantiles()), function(d) { return d; })
    .enter().append("g")
    .attr("class", "legend");

    legend.append("rect")
    .attr("x", function(d, i) { return cellSize * (i-1)-20; })
    .attr("y", height-50)
    .attr("width", cellSize)
    .attr("height", cellSize/2)
    .style("stroke","#d9d9d9")
    .style("fill", function(d, i) { return colors[i]; });

    legend.append("text")
    .attr("class", "mono")
    .text(function(d) { return Math.round(d); })
    .attr("x", function(d, i) { return cellSize * (i-1)-20; })
    .attr("y", height-50+cellSize/1.5);

    legend.exit().remove();
  });
}
heatmap("#area",2011)
onchange = function (){
  //var sect = document.getElementById("inds");
  //var section = sect.options[sect.selectedIndex].value;
  d3.select('svg').remove()
  section = d3.select('select').property('value')
  heatmap("#area",section);
}