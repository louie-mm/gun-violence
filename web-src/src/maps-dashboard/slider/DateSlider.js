import noUiSlider from 'nouislider';
import React from 'react';
import './slider.scss';
import { formatDate, yymmddToUnix } from './utils/date.js'


export default class DateSlider extends React.Component {
	constructor(props) {
    super(props);
    this._addSliderCssLink();
  }

  componentDidMount() {
    this._createSlider(yymmddToUnix(this.props.startDate), yymmddToUnix(this.props.endDate) - 86400, this.refs.dateSlider)
    this._onMoveSliderHandles(this.refs.dateSlider);
  }

  render() {
    return (
      <div ref='dateSlider' className="noUiSlider" id={this.props.id}></div>
    )
  }

  _addSliderCssLink() {
    if(!document.getElementById('noUiSliderCssLink')) {
      var link = document.createElement('link');
      link.id = 'noUiSliderCssLink';
      link.rel = 'stylesheet';
      link.href = 'https://cdnjs.cloudflare.com/ajax/libs/noUiSlider/11.1.0/nouislider.css';
      document.head.appendChild(link);
    }
  }

  _createSlider(unixStartDate, unixEndDate, dateSliderRef) {
    noUiSlider.create(dateSliderRef, {
      range: {
        'min': unixStartDate,
        'max': unixEndDate
      },
      start: [unixStartDate, unixStartDate],
      connect: true,
      orientation: 'horizontal',
      behaviour: 'tap',
      tooltips: true,
    })
  }

  _onMoveSliderHandles(dateSliderRef) {
    self = this;
    var sliderTooltips = this._getSliderTooltips();
    dateSliderRef.noUiSlider.on('update', function(values, handle) {
      self.props.filterDataBySelectedDates(+values[0], +values[1]);
      sliderTooltips[handle].innerHTML = formatDate(new Date(+values[handle] * 1000));
    })
  }

  _getSliderTooltips() {
    return document.getElementById(this.props.id).getElementsByClassName('noUi-tooltip');
  }
}