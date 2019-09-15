//
var margin = {top: 20, right: 230, bottom: 100, left: 150},
width = 1250 - margin.left - margin.right,
height = 480 - margin.top - margin.bottom,
padding = 15;
//Load the data
var data = [
{country: 'Bangladesh', population_2012: 105905297, growth: {year_2013:42488 , year_2014:934 , year_2015:52633 , year_2016:112822 , year_2017:160792}},
{country: 'Ethopia', population_2012: 75656319, growth: {year_2013:1606010 , year_2014:1606705 , year_2015:1600666 , year_2016:1590077 , year_2017:1580805}},
{country: 'Kenya', population_2012: 33007327, growth: {year_2013:705153 , year_2014:703994 , year_2015:699906 , year_2016:694295 , year_2017:687910}},
{country: 'Afghanistan', population_2012: 23280573, growth: {year_2013:717151 , year_2014:706082 , year_2015:665025 , year_2016:616262 , year_2017:573643}},
{country: 'Morocco', population_2012: 13619520, growth: {year_2013:11862 , year_2014:7997 , year_2015:391 , year_2016:-8820 , year_2017:-17029}}
];
//process the data
var format = data.map(function(d){
    var base = [d.population_2012, d.growth.year_2013, d.growth.year_2014, d.growth.year_2015,
    d.growth.year_2016,  d.growth.year_2017]

    var cum_sum = []
    base.reduce(function(a,b,i){return cum_sum[i] = a+b;},0)

    var percent = base.slice(1,6).map(function(d,i){
        return d*100/cum_sum[i]
    })
    var total = cum_sum[5]

    return{
        name:d.country,
        value:d3.zip(["2013","2014","2015","2016","2017"],percent),
        total:total
    }
});

//add svg
var svg = d3.select(".main")
.append("svg:svg")
.attr("width", width + margin.left + margin.right)
.attr("height", height + margin.top + margin.bottom)
.append("g")
.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

//create x scale
var x = d3.scaleLinear()
.range([0, width])
.domain([0, d3.max(format, function(d) {
    return d.total;
})])
.nice();

//create y scale
var y = d3.scaleBand()
.rangeRound([0, height], 0.1)
.domain(format.map(function (d) {
    return d.name;
}));

//create y axis
var yAxis = d3.axisLeft(y)
.tickPadding(10);

//add bar
var bar = svg.selectAll(".bar")
.data(format)
.enter().append("g")
.attr("class", "bar")
.attr("transform", function(d) {
    return "translate(0," + (y(d.name)+padding*0.5) + ")";
});

bar.append("rect")
.attr("width", function (d) { return x(d.total); })
.attr("height", y.bandwidth()-padding)
.on("mouseover", showLegend)
.on("mouseout", offLegend);
var text = bar.append("text")
.attr("class", "bar")
.attr("x", 10)
.attr("y", y.bandwidth()*0.5-padding*0.5)
.attr("dy", ".35em")
.text(function(d){
  return d.total.toLocaleString();
})
text.on("mouseover", showLegend)
.on("mouseout", offLegend);

//add y axis
svg.append("g")
.attr("class", "y axis")
.call(yAxis);

var legend = svg.append("g")
.attr("transform", "translate(" + (width + 30) + ", " + (height-350) + ")")
.attr("class", ".legend");


function showLegend(data) {
    d3.selectAll(".lchart").remove();
    d3.select(this).style("fill", "#0868ac");
    text.style("fill", "white");
    var lchart = svg.append("svg")
    .attr("class", "lchart")
    .attr("height", height + margin.top + margin.bottom)
    .attr("width", width + margin.left + margin.right)
    .append("g")
    .attr("transform", "translate(600,160)");

    var x2 = d3.scaleLinear().domain([2013, 2017]).range([0, 250]);
    var y2 = d3.scaleLinear().domain([d3.min(data.value, function(d) {
        return d[1];}),d3.max(data.value, function(d) {return d[1]; })])
    .range([200, 0]);

    var xAxis2 = d3.axisBottom(x2)
    .ticks(5)
    .tickFormat(d3.format("d"));
    var yAxis2 = d3.axisLeft(y2)
    .ticks(5);

    lchart.append("g")
    .attr("class", "axis2")
    .attr("transform", "translate(0, 200)")
    .call(xAxis2);
    
    lchart.append("g")
    .attr("class", "axis2")
    .call(yAxis2);
    var line = d3.line()
    .x(function(d) {
        return x2(d[0]); 
    })
    .y(function(d) { 
        return y2(d[1]); 
    });

    lchart.append("path")
    .attr("d", line(data.value))
    .style("stroke", "#0868ac")
    .style("stroke-width", 2)
    .style("fill", "none");

    //Add x-axis label
    lchart.append("text")
    .attr("y",200)
    .attr("x",250)
    .style("text-anchor","start")
    .style("font-size","14px")
    .text("Year");

    //Add y-axis label
    lchart.append("text")
    .attr("y",0)
    .attr("x",-2)
    .attr("dy","-0.3em")
    .style("text-anchor","end")
    .style("font-size","14px")
    .text("Pct %")
};

function offLegend(){
    d3.selectAll(".lchart").remove();
    d3.select(this).style("fill", "#4eb3d3");
    text.style("fill", "white")
}
