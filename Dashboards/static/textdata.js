function drawtext(error, data){
    
    d3.select("#text1 svg").remove();
    var svg1 = d3.select("#text1").append("svg")
                                     .attr("width",376)
                                      .attr("height",348);

  // var text1 = svg1.append("text").attr("x",170).attr("y",30).text("Incidents").attr("fill","#ccc").attr("stroke","#ccc").attr("text-anchor","middle")
  // .style("font-size", "22px");

  // svg1.append("text").attr("x",170).attr("y",80).text(data.incidents).attr("text-anchor","middle")
  // .style("font-size", "55px").style("fill","#FF884D");

  svg1.append("text").attr("x",100).attr("y",50).text("Country").attr("fill","#000").attr("stroke","#000").attr("text-anchor","middle")
  .style("font-size", "20px");

  svg1.append("text").attr("x",100).attr("y",100).text(data.Country).attr("text-anchor","middle")
  .style("font-size", "32px").style("fill","#cc0000");

  svg1.append("text").attr("x",100).attr("y",150).text("Sufferings").attr("fill","#000").attr("stroke","#000").attr("text-anchor","middle")
  .style("font-size", "20px");

  svg1.append("text").attr("x",100).attr("y",200).text(data.sufferings).attr("text-anchor","middle")
  .style("font-size", "32px").style("fill","#cc0000");

  svg1.append("text").attr("x",100).attr("y",250).text("Deaths").attr("fill","#000").attr("stroke","#000").attr("text-anchor","middle")
  .style("font-size", "20px");

  svg1.append("text").attr("x",100).attr("y",300).text(data.deaths).attr("text-anchor","middle")
  .style("font-size", "32px").style("fill","#cc0000");

}


d3.queue().defer(d3.json, "/getTextData?country=All")
.await(drawtext);
