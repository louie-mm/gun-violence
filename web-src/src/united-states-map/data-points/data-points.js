import * as d3 from 'd3';


// TODO: Would be good if we can find a way to have deaths on top and injuries underneatd.
// Since we can't use Z-index, alternatives could be use, wrap svg elements in divs and z-index the div
// or sorting the dom elements directly and potentially using .front()
export default function enter(svg, data, projection) {

  let circle = svg.selectAll("circle")
    .data(data, function(d) {return d.longitude.toString() + d.latitude.toString() + d.date.$date.toString() + d.type});

  circle.exit()
    .remove();

  circle.enter()
    .append("circle")
    .attr("cx", function(d) {
      return projection([d.longitude, d.latitude])[0];
    })
    .attr("cy", function(d) {
      return projection([d.longitude, d.latitude])[1];
    })
    .attr('class', function(d) {return d.type})
    .transition()
    .duration(1000)
    .ease(d3.easeBackOut.overshoot(10))
    .attr("r",function(d) {
      return Math.sqrt(d.number) * 5;
    });
}