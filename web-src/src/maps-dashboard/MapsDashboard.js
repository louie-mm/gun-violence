import React from 'react';
import UnitedStatesMap from './united-states-map/UnitedStatesMap.js';
import DateSlider from './slider/DateSlider.js';
import Analytics from './analytics/Analytics.js'
import RightHandPanel from './right-hand-panel/RightHandPanel.js';
import './maps-dashboard.scss';

import { unixToYymmdd } from './slider/utils/date.js';

export default class MapsDashboard extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      filteredData: null,
      isMapLoaded: false,
    }

    this.unitedStatesMap = React.createRef();

    this._setMapLoadedStateToTrue = this._setMapLoadedStateToTrue.bind(this);
    this._filterDataBySelectedDates = this._filterDataBySelectedDates.bind(this);
  }

  render() {
    return (
      <div>
        <div className="maps-dashboard">
          <div id="united-states-map" ref={this.unitedStatesMap}>
            {this.state.filteredData &&
              <UnitedStatesMap
                data={this.state.filteredData}
                width={this.unitedStatesMap.current.offsetWidth}
                height={this.unitedStatesMap.current.offsetWidth / 2}
                options={{
                  'setMapLoadedStateToTrue': this._setMapLoadedStateToTrue,
                  'isDataFiltered': this.state.filteredData != null
                }}
              />
            }
          </div>
          <div className="right-hand-panel">
            <RightHandPanel
              data={this.state.filteredData}
            />
          </div>
        </div>
        <DateSlider
          startDate={this._getStartDate()}
          endDate={this._getEndDate()}
          id={'united-states-map-date-slider'}
          filterDataBySelectedDates={this._filterDataBySelectedDates}
        />
    </div>
    );
  }

  _setMapLoadedStateToTrue() {
    this.setState({
      isMapLoaded: true
    });
  }

  _getStartDate() {
    return this.props.startDate;
  }

  _getEndDate() {
    return this.props.endDate;
  }

  // _getStartDate() {
  //   return this.props.data[0].date.$date + 86400;
  // }

  // _getEndDate() {
  //   return this.props.data[this.props.data.length - 1].date.$date - 86400;
  // }

  _filterDataBySelectedDates(unixStartDate, unixEndDate) {
    // const filteredData = this.props.data.filter( incident => 
    //   incident.date.$date >= startDate && incident.date.$date <= endDate
    // );
    // this.setState({
    //   filteredData: filteredData
    // });
    let filteredData = [];
    let currentDate = unixToYymmdd(unixStartDate);
    const allData = this.props.data;
    while(currentDate <= unixToYymmdd(unixEndDate)) {
      Array.prototype.push.apply(filteredData, allData[currentDate]['incidents']);
      currentDate = allData[currentDate]['next'];
    }
    this.setState({
      filteredData: filteredData
    });
  }
}