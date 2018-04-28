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
      data: null
    }
  }

  componentDidMount() {
    let data;
    if(config.readStaticData) {
      data = this._readStaticData();
    } else {
      data = this._loadData();
    }
  }

  render() {
    return (
      <div id="maps-dashboard-container">
      {this.state.data && (
        <MapsDashboard
          data={this.state.data}
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
        this.setState({
          data: response.data
        })
      },
      error => {
        console.log(error);
        return error;
      }
    )
  }
}