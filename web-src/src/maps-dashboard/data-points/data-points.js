import * as d3 from 'd3';  //TODO: Only import the necessary libs
import config from './config.json';
import easeAbstractFactory from './easeFactory';

// TODO: Would be good if we can find a way to have deaths on top and injuries underneath.
// Since we can't use Z-index, alternatives could be use, wrap svg elements in divs and z-index the div
// or sorting the dom elements directly and potentially using .front()
export function appendDataPoints(svg, data, projection) {
  const ease = easeAbstractFactory();
  const duration = config.transitionDurationInMilliseconds;
  const dataPointSize = config.dataPointSize;

  let circle = svg.selectAll("circle")
    .data(data, function(d) {return d.id});

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
    .duration(duration)
    .ease(ease)
    .attr("r",function(d) {
      return Math.sqrt(d.number) * dataPointSize;
    });
}

export function resizeDataPoints(svg, projection) {

  let circle = svg.selectAll("circle")
    .attr("cx", function(d) {
      return projection([d.longitude, d.latitude])[0];
    })
    .attr("cy", function(d) {
      return projection([d.longitude, d.latitude])[1];
    });
}