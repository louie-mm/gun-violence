import d3Wrap from 'react-d3-wrap';
import * as d3 from 'd3';  //TODO: Only import the necessary libs
import './united-states-map.scss';
import { appendDataPoints, resizeDataPoints } from '../data-points/data-points.js';
import * as topojson from "topojson-client";  //TODO: Only import the necessary libs
import usaTopo from './usa-topo.json'


const UnitedStatesMap = d3Wrap({
  initialize(svg, data, options) {
    const width = +svg.getAttribute('width');
    const height = +svg.getAttribute('height');
    const projection = this._getUsaProjection(width, height);
    const path = this._getPathFromProjection(projection);

    d3.select(svg)
      .selectAll("path")
      .data(topojson.feature(usaTopo, usaTopo.objects.USA_adm1).features)
      .enter()
      .append("path")
      .attr("d", path)
      .attr('class', 'map');

    options.setMapLoadedStateToTrue();

    window.addEventListener("resize", this._resize.bind(this));
  },

  update (svg, data, options) {
    if(!options.isDataFiltered) return;
    const width = +svg.getAttribute('width');
    const height = +svg.getAttribute('height');
    const projection = this._getUsaProjection(width, height);
    appendDataPoints(d3.select(svg), data, projection)
  },

  _getUsaProjection(width, height) {
    return d3.geoAlbersUsa()
      .translate([width/2, height/2])
      .scale(width); 
  },

  _getPathFromProjection(projection) {
    return d3.geoPath()
       .projection(projection);
  },

  _resize() {
    const width = document.getElementById('united-states-map').offsetWidth;
    const height = width / 2;
    const newProjection = this._getUsaProjection(width, height);
    const newPath  = this._getPathFromProjection(newProjection);
    const svg = d3.select('svg');

    svg.style('width', width + 'px')
      .style('height', height + 'px');

    svg.selectAll('path')
      .attr('d', newPath)

    resizeDataPoints(svg, newProjection);
  }
});

export default UnitedStatesMap;
