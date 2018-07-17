import React from 'react';
import './dial.scss';
import deathCount from './death-count.json';
import config from './config.json';

export default class Dial extends React.Component {
	constructor(props) {
		super(props);
	}

	render() {
		let rows = [];
		const pixelsPerDeath = (config.innerSliderHeight - 2*config.innerSliderPadding) / this.props.totalDeaths;
		const innerSliderStyle = {
			height: config.innerSliderHeight + "px",
			transform: "translateY(" + -(config.innerSliderHeight - 2*config.innerSliderPadding - pixelsPerDeath*this.props.totalDeathsToDate) + "px)"
		}

		deathCount.forEach(function(event) {
			rows.push(
		    	<p
	    		className="events"
	    		id={"death-count-"+event.event}
	    		key={event.event}
	    		style={{position: 'absolute', 'bottom': config.innerSliderPadding + pixelsPerDeath * event.deaths + 'px'}}
	    		>
		    		{event.event + ": " + event.deaths + " deaths"}
		    	</p>
		    );
		});
		return (
			<div className="outside">
				<div style={innerSliderStyle} className="inside">
					{rows}
				</div>
			</div>
		)
	}
}