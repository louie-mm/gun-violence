import d3Wrap from 'react-d3-wrap';
import * as d3 from 'd3';
import './united-states-map.scss';
import enter from './data-points/data-points.js';
// import Topojson from './USA_adm.json';


const UnitedStatesMap = d3Wrap({
  initialize(svg, data, options) {
    const width = +svg.getAttribute('width');
    const height = +svg.getAttribute('height');

    let projection = d3.geoAlbersUsa()
      .translate([width/2, height/2])
      .scale([1000]); 

    let path = d3.geoPath()
       .projection(projection);

    d3.json("http://localhost:8080/united-states-map/usa-geo.json", function(error, json) {
      d3.select(svg)
        .selectAll("path")
        .data(json.features)
        .enter()
        .append("path")
        .attr("d", path)
        .attr('class', 'geojson');

      options.setMapLoadedStateToTrue();
    });
  },

  update (svg, data, options) {
    if(!options.isDataFiltered) return;

    const width = +svg.getAttribute('width');
    const height = +svg.getAttribute('height');

    let projection = d3.geoAlbersUsa()
      .translate([width/2, height/2])
      .scale([1000]);

    this._appendDataPoints(d3.select(svg), data, projection)
  },

  destroy () {
    // Optional clean up when a component is being unmounted... 
  },

  _appendDataPoints(svg, data, projection) {
    enter(svg, data, projection);
  }
});

export default UnitedStatesMap;