import React from 'react';
import Dial from './dial/Dial.js';

export default class RightHandPanel extends React.Component {
	constructor(props) {
		super(props);
	}

	render() {
		return (
			<div id="right-hand-panel">
				<Dial
					totalDeaths={this.props.totalDeaths}
					totalDeathsToDate={this.props.totalDeathsToDate}
				/>
			</div>
		)
	}
}