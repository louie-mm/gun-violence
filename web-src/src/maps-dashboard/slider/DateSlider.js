import noUiSlider from 'nouislider';
import React from 'react';
import './slider.scss';
import formatDate from './utils/date.js'


export default class DateSlider extends React.Component {
	constructor(props) {
    super(props);
    this._addSliderCssLink();
  }

  componentDidMount() {
    const startDate = this.props.startDate;
    const endDate = this.props.endDate;
    const dateSlider = this.refs.dateSlider;

    this._createSlider(startDate, endDate, dateSlider)
    this._onMoveSliderHandles(dateSlider)    
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

  _createSlider(startDate, endDate, dateSliderRef) {
    noUiSlider.create(dateSliderRef, {
      range: {
        'min': startDate,
        'max': endDate
      },
      start: [startDate, startDate],
      connect: true,
      orientation: 'horizontal',
      behaviour: 'tap',
      tooltips: true,
    })
  }

  // TODO: Lot's of room for improvement in this function
  _onMoveSliderHandles(dateSliderRef) {
    self = this;
    var sliderTooltips = this._getSliderTooltips();
    dateSliderRef.noUiSlider.on('update', function(values, handle) {
      self.props.filterDataBySelectedDates(+values[0], +values[1]);
      sliderTooltips[handle].innerHTML = formatDate(new Date(+values[handle]));
    })
  }

  _getSliderTooltips() {
    return document.getElementById(this.props.id).getElementsByClassName('noUi-tooltip');
  }
}