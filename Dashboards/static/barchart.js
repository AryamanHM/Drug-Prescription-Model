
function drawbarchart(erorr,ddata){
    console.log("ddata-->",ddata);
    data= JSON.parse(ddata);

// set the dimensions and margins of the graph
var margin = {top: 25, right: 30, bottom: 40, left: 80},
width = 500 - margin.left - margin.right,
height = 300 - margin.top - margin.bottom;

// set the ranges
var y = d3.scaleBand()
      .range([height, 0])
      .padding(0.1);

var x = d3.scaleLinear()
      .range([0, width]);
      
// append the svg object to the body of the page
// append a 'group' element to 'svg'
// moves the 'group' element to the top left margin
var svg = d3.select("#barchart").append("svg")
.attr("width", width + margin.left + margin.right)
.attr("height", height + margin.top + margin.bottom)
.append("g")
.attr("transform", 
      "translate(" + margin.left + "," + margin.top + ")");


      svg.append("text")
      .attr("x", (width / 2))             
      .attr("y", -13 )
      .attr("text-anchor", "middle")  
      .style("font-size", "16px")
      .style("fill","#000") 
      .style("text-decoration", "underline")  
      .text("Age Group");


// format the data
data.forEach(function(d) {
d.count = +d.count;
console.log("count")
console.log(d.count)

});

// Scale the range of the data in the domains
x.domain([0, d3.max(data, function(d){ return d.count; })])
y.domain(data.map(function(d) { return d.age; }));
//y.domain([0, d3.max(data, function(d) { return d.sales; })]);

// append the rectangles for the bar chart
svg.selectAll(".bar")
  .data(data)
.enter().append("rect")
    .transition()
    .duration(700)
  .attr("class", "bar")
  //.attr("x", function(d) { return x(d.sales); })
  .attr("width", function(d) {return x(d.count); } )
  .attr("y", function(d) { return y(d.age); })
  .attr("height", y.bandwidth())
  .attr("fill","#ff6500");

// add the x Axis
svg.append("g")
  .attr("transform", "translate(0," + height + ")")
  .attr("fill","#000")
  .attr("text","#000")
  .call(d3.axisBottom(x))
  .selectAll("text")
  .style("text-anchor", "end")
        .attr("dx", "-.8em")
        .attr("dy", ".15em")
        .attr("transform", "rotate(-30)");

// add the y Axis
svg.append("g")
  .call(d3.axisLeft(y));


  

}


//var bardata = [{"wtype":"Unknown","countt":33},{"wtype":"Robin","countt":12},{"wtype":"Incendiary","countt":22},{"wtype":"Chemical","countt":4}];
d3.queue().defer(d3.json, "/getDataPerCountryBar?country=All")
.await(drawbarchart);
