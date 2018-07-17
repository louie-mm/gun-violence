import React from 'react';
import getData from './requests/requestHandler.js';
import MapsDashboard from './maps-dashboard/MapsDashboard.js';
import config from './config.json';
import staticShootingsData from './static-shootings-data.json';
import './maps-dashboard-container.scss';

export default class MapsDashboardContainer extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      data: null,
      startDate: null,
      endDate: null,
      totalDeaths: null,
      totalInjuries: null
    }
  }

  componentDidMount() {
    config.readStaticData ? this._readStaticData() : this._loadData();
  }

  render() {
    return (
      <div id="maps-dashboard-container">
      {this.state.data && (
        <MapsDashboard
          data={this.state.data}
          startDate={this.state.startDate}
          endDate={this.state.endDate}
          totalDeaths={this.state.totalDeaths}
          totalInjuries={this.state.totalInjuries}
        />
      )}
      </div>
    );
  }

  _readStaticData() {
    this.setState({
      data: staticShootingsData
    })
  }

  _loadData() {
    getData(
      response => {
        const responseBody = response.data;
        this.setState({
          data: responseBody.data,
          startDate: responseBody.startDate,
          endDate: responseBody.endDate,
          totalDeaths: responseBody.totalDeaths,
          totalInjuries: responseBody.totalInjuries
        })
      },
      error => {
        console.log(error);
        return error;
      }
    )
  }
}