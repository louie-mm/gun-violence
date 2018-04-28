import d3Wrap from 'react-d3-wrap';
import * as d3 from 'd3';  //TODO: Only import the necessary libs
import './united-states-map.scss';
import appendDataPoints from '../data-points/data-points.js';
import * as topojson from "topojson-client";  //TODO: Only import the necessary libs


const UnitedStatesMap = d3Wrap({
  initialize(svg, data, options) {
    const projection = this._getUsaProjection(svg);

    let path = d3.geoPath()
       .projection(projection);

    // TODO: find a way to import the file with ES6, that way we won't need to grab the resource as a served file
    d3.json("http://localhost:8080/maps-dashboard/united-states-map/usa-topo.json", function(error, json) {
      d3.select(svg)
        .selectAll("path")
        .data(topojson.feature(json, json.objects.USA_adm1).features)
        .enter()
        .append("path")
        .attr("d", path)
        .attr('class', 'map');

      options.setMapLoadedStateToTrue();
    });
  },

  update (svg, data, options) {
    if(!options.isDataFiltered) return;
    const projection = this._getUsaProjection(svg);
    appendDataPoints(d3.select(svg), data, projection)
  },

  destroy () {
    // Optional clean up when a component is being unmounted... 
  },

  _getUsaProjection(svg) {
    const width = +svg.getAttribute('width');
    const height = +svg.getAttribute('height');

    return d3.geoAlbersUsa()
      .translate([width/2, height/2])
      .scale(width); 
  }
});

export default UnitedStatesMap;