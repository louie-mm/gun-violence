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
      totalDeathsToDate: 0,
      totalInjuriesToDate: 0,
      isMapLoaded: false,
      filteredDataStartDate: this._getStartDate(),
      filteredDataEndDate: this._getStartDate()
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
              totalDeaths={this.props.totalDeaths}
              totalDeathsToDate={this.state.totalDeathsToDate}
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

  _filterDataBySelectedDates(unixStartDate, unixEndDate) {
    let filteredData = [];
    const currentDateForD3 = +unixToYymmdd((unixEndDate - 604800) < unixStartDate ? unixStartDate : unixEndDate - 604800);
    let currentDate = +unixToYymmdd(unixStartDate);
    const allData = this.props.data;
    let totalDeathsToDate = 0;
    let totalInjuriesToDate = 0;
    while(currentDate <= +unixToYymmdd(unixEndDate)) {
      if(currentDate >= currentDateForD3) Array.prototype.push.apply(filteredData, allData[currentDate]['incidents']);
      totalDeathsToDate += allData[currentDate]['totalDeathsForDate'];
      totalInjuriesToDate += allData[currentDate]['totalInjuriesForDate'];
      currentDate = allData[currentDate]['next'];
    }
    this.setState({
      filteredData: filteredData,
      filteredDataStartDate: +unixToYymmdd(unixStartDate),
      filteredDataEndDate: +unixToYymmdd(unixEndDate),
      totalDeathsToDate: totalDeathsToDate,
      totalInjuriesToDate: totalInjuriesToDate
    });
  }
}
