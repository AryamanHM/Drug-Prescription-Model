

 
var width2 = 730 ,
height2 = 330
active = d3.select(null);


var projection = d3.geoMercator()
  .scale(120)
  .center([0,20])
  .translate([width2 / 2, height2 / 2]);


var zoom = d3.zoom().on("zoom", zoomed);
var path = d3.geoPath();
  
// The svg
var svg2 = d3.select("#mapdiv").append("svg")
.attr("width", width2 )
.attr("height", height2 )
.on("click", stopped, true);

svg2.append("rect")
    .attr("class", "background")
    .attr("width", width2)
    .attr("height", height2)
    .on("click", reset);

var g = svg2.append('g'); 

var tip = d3.tip()
            .attr('class', 'd3-tip')
            .offset([-10, 0])
            .html(function(d) {
              return "<strong>Country: </strong><span class='details'>" + d.properties.name + "<br></span>" + "<strong>Drug Usage: </strong><span class='details'>" + d.total +"</span>";
            })


  svg2.call(zoom);          
  svg2.call(tip); 



// Data and color scale
var data = d3.map();
var colorScale = d3.scaleThreshold()
.domain([10000,100000,500000,1000000,5000000,10000000,50000000,100000000,500000000,1500000000])
.range(d3.schemeYlOrBr[9]);


//.range(['#f6f2ff','#f6f2ff','#e8daff','#e8daff','#d4bbff','#d4bbff','#be95ff','#be95ff','#a56eff','#8a3ffc']);

var x = svg2.append("g")
        .attr("class", "legendThreshold")
        .attr("transform", "scale(0.7) translate(30,300)");
        // .attr("width", 200)
        // .attr("height", 200);

    var labels = ["0-10k", "10k-100k", "100k-500k", "500K-1M", "1M-5M", "5M-10M", "10M-50M", "50M-100M", "100M +"];
    var legend = d3.legendColor()
        .labels(function (d) { return labels[d.i]; })
        .shapePadding(0)
        .scale(colorScale);
    svg2.select(".legendThreshold")
        .call(legend);


// Load external data and boot
d3.queue()
  .defer(d3.json, "https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson")
  .defer(d3.csv, "static/map.csv", function(d) { data.set(d.Code, +d.cases); })
  .await(ready);

console.log(data)
  
function ready(error, topo) {

  console.log(topo)

  let mouseOver = function(d) {
    d3.selectAll(".Country")
      .transition()
      .duration(200)
      .style("opacity", .5)
    d3.select(this)
      .transition()
      .duration(200)
      .style("opacity", 1)
      .style("stroke", "red")
    tip.show(d)
  }



  let mouseLeave = function(d) {
    d3.selectAll(".Country")
      .transition()
      .duration(200)
      .style("opacity", 1)
    d3.select(this)
      .transition()
      .duration(200)
      .style("stroke", "transparent")
      tip.hide(d) 
  }

  let clickevent = function(d){

    country=d.id
    country1= country.toString()
    
    d3.queue().defer(d3.json, "/getDataPerCountryPie?country="+country1).await(drawpie);
    d3.queue().defer(d3.json, "/getDataPerCountryBar?country=" + country1).await(updatebarchart);
    d3.queue().defer(d3.json, "/getDataSun?country="+country1).await(drawsunburst);
    d3.queue().defer(d3.json, "/getTextData?country=" + country1).await(drawtext);

     
  }

  // Draw the map
 

  
    g.selectAll("path")
    .data(topo.features)
    .enter()
    .append("path")
      // draw each country
      .attr("d", d3.geoPath()
        .projection(projection)
      )
      // set the color of each country
      .attr("fill", function (d) {
        d.total = data.get(d.id) || 0;
        return colorScale(d.total);
      })
      .style("stroke", "transparent")
      .attr("class", function(d){ return "Country" } )
      .style("opacity", .8)
      .on("mouseover", mouseOver )
      .on("mouseleave", mouseLeave )
      .on("click", clickevent );
    }



    function clicked(d) {
      if (active.node() === this) return reset();
      active.classed("active", false);
      active = d3.select(this).classed("active", true);
    
      var bounds = path.bounds(d),
          dx = bounds[1][0] - bounds[0][0],
          dy = bounds[1][1] - bounds[0][1],
          x = (bounds[0][0] + bounds[1][0]) / 2,
          y = (bounds[0][1] + bounds[1][1]) / 2,
          scale = Math.max(1, Math.min(8, 0.9 / Math.max(dx / width2, dy / height2))),
          translate = [width2 / 2 - scale * x, height2 / 2 - scale * y];
    
      svg2.transition()
          .duration(750)
          // .call(zoom.translate(translate).scale(scale).event); // not in d3 v4
          .call( zoom.transform, d3.zoomIdentity.translate(translate[0],translate[1]).scale(scale) ); // updated for d3 v4
    }
    
    function zoomed() {
      g.style("stroke-width", 1.5 / d3.event.transform.k + "px");
      // g.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")"); // not in d3 v4
      g.attr("transform", d3.event.transform); // updated for d3 v4
    }

    function reset() {

      d3.queue().defer(d3.json, "/getDataPerCountryPie?country=All")
.await(drawpie);

      d3.queue().defer(d3.json, "/getDataPerCountryBar?country=All")
.await(updatebarchart);

d3.queue().defer(d3.json, "/getDataSun?country=All")
.await(drawsunburst);

d3.queue().defer(d3.json, "/getTextData?country=All")
.await(drawtext);



      active.classed("active", false);
      active = d3.select(null);
    
      svg2.transition()
          .duration(750)
          // .call( zoom.transform, d3.zoomIdentity.translate(0, 0).scale(1) ); // not in d3 v4
          .call( zoom.transform, d3.zoomIdentity ); // updated for d3 v4
    }
    function stopped() {
      if (d3.event.defaultPrevented) d3.event.stopPropagation();
    }
