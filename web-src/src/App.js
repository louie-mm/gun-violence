import React from 'react';
import getData from './requests/requestHandler.js';
import Display from './Display.js'

export default class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      data: null
    }
    this._loadData();
  }

  render() {
    return (
      <div>
      {this.state.data != null && (
        <Display
          data={this.state.data}
        />
      )}
      </div>
    );
  }

  _loadData() {
    getData(
      response => {
        this.setState({
          data: response.data
        });
      },
      error => {
        console.log(error);
      }
    )
  }
}