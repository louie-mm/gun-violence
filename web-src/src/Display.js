import React from 'react';
import UnitedStatesMap from './united-states-map/UnitedStatesMap.js';
import DateSlider from './slider/DateSlider.js';
import Analytics from './analytics/Analytics.js'

export default class Display extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      filteredData: null,
      isMapLoaded: false,
    }

  this._setMapLoadedStateToTrue = this._setMapLoadedStateToTrue.bind(this);
  this._filterDataBySelectedDates = this._filterDataBySelectedDates.bind(this);
  }

  render() {
    return (
      <div>
        {/*this.state.isMapLoaded &&
          <Analytics
          data={this.state.filteredData}
        />
        */}
        {this.state.filteredData &&
        <UnitedStatesMap
        // TODO: This is generating a warning since it's undefined. Maybe there's a good way around this problem
          data={this.state.filteredData}
          width={document.getElementById('app').offsetWidth}
          height={document.getElementById('app').offsetWidth / 2}
          options={{
            'setMapLoadedStateToTrue': this._setMapLoadedStateToTrue,
            'isDataFiltered': this.state.filteredData != null
          }}
        />
        }
        {true &&
        <DateSlider
          startDate={this._getStartDate()}
          endDate={this._getEndDate()}
          id={'united-states-map-date-slider'}
          filterDataBySelectedDates={this._filterDataBySelectedDates}
        />
        }
      </div>
    );
  }

  _setMapLoadedStateToTrue() {
    this.setState({
      isMapLoaded: true
    });
  }

  _getStartDate() {
    return this.props.data[0].date.$date + 86400;
  }

  _getEndDate() {
    return this.props.data[this.props.data.length - 1].date.$date - 86400;
  }

  _filterDataBySelectedDates(startDate, endDate) {
    const filteredData = this.props.data.filter( incident => 
      incident.date.$date >= startDate && incident.date.$date <= endDate
    );
    this.setState({
      filteredData: filteredData
    });
  }
}