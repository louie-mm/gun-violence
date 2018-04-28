import React from 'react';

export default class Analytics extends React.Component {
	constructor(props) {
    super(props);

    this.state = {
      numberOfDeaths: 0,
      numberOfInjuries: 0
    }
  }

  getDerivedStateFromProps(nextProps) {
    this._findNumberOfDeathsAndInjuries(nextProps);
  }

  render() {
    return (
      <div className="analytics-container">
        <div className="analytics-row">
          <div className="field">Deaths: </div>
          <div className="value">{this.state.numberOfDeaths}</div>
        </div>
        <div className="analytics-row">
          <div className="field">Injuries: </div>
          <div className="value">{this.state.numberOfInjuries}</div>
        </div>
      </div>
    );
  }

  _findNumberOfDeathsAndInjuries(nextProps) {

    nextProps.forEach(function(element) {
      let killed = 0;
      let injured = 0;
      if(element.type === 'injured') injured++;
      else if(element.type === 'killed') killed++;
    })
    this.setState({
      numberOfDeaths: killed,
      numberOfInjuries: injured
    })
  }
}