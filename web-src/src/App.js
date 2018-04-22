import React from 'react';
import getData from './requests/requestHandler.js';
import Display from './Display.js';
import config from './config.json';
import staticShootingsData from './static-shootings-data.json';

export default class App extends React.Component {
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

    this.setState({
      data: data
    })
  }

  render() {
    return (
      <div>
      {this.state.data !== null && (
        <Display
          data={this.state.data}
        />
      )}
      </div>
    );
  }

  _readStaticData() {
    return staticShootingsData;
  }

  _loadData() {
    getData(
      response => {
        return response.data;
      },
      error => {
        console.log(error);
      }
    )
  }
}