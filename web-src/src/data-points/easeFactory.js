import * as d3 from 'd3';
import config from './config.json';


export default function easeAbstractFactory() {
	switch(config.transitionEaseType) {
		case "poly": return polyFactory();
		case "sin": return sinFactory();
		case "exp": return polyFactory();
		case "circle": return circleFactory();
		case "elastic": return elasticFactory();
		case "back": return backFactory();
		case "bounce": return bounceFactory();
		default: console.log("You done fucked up!");
	}
}

function polyFactory() {
	const polyExponent = config.transitionEaseMagnitude;
	switch(config.transitionEaseDirection) {
		case "in": return d3.easePolyIn.exponent(polyExponent);
		case "out": return d3.easePolyOut.exponent(polyExponent);
		case "inout": return d3.easePolyInOut.exponent(polyExponent);
		default: console.log("You done fucked up!");
	}
}

function sinFactory() {
	switch(config.transitionEaseDirection) {
		case "in": return d3.easeSinIn;
		case "out": return d3.easeSinOut;
		case "inout": return d3.easeSinInOut;
		default: console.log("You done fucked up!");
	}
}

function expFactory() {
	switch(config.transitionEaseDirection) {
		case "in": return d3.easeExpIn;
		case "out": return d3.easeExpOut;
		case "inout": return d3.easeExpInOut;
		default: console.log("You done fucked up!");
	}
}

function circleFactory() {
	switch(config.transitionEaseDirection) {
		case "in": return d3.easeCircleIn;
		case "out": return d3.easeCircleOut;
		case "inout": return d3.easeCircleInOut;
		default: console.log("You done fucked up!");
	}
}

function elasticFactory() {
	let elasticEase;
	switch(config.transitionEaseDirection) {
		case "in": return d3.easeElasticIn; break;
		case "out": return d3.easeElasticOut; break;
		case "inout": return d3.easeElasticInOut; break;
		default: console.log("You done fucked up!");
	}
	elasticEase.amplitude(config.transitionEaseMagnitude);
	elasticEase.period(config.transitionEasePeriod);
	return elasticEase;
}

function backFactory() {
	const backOvershoot = config.transitionEaseMagnitude;
	switch(config.transitionEaseDirection) {
		case "in": return d3.easeBackIn.overshoot(backOvershoot);
		case "out": return d3.easeBackOut.overshoot(backOvershoot);
		case "inout": return d3.easeBackInOut.overshoot(backOvershoot);
		default: console.log("You done fucked up!");
	}
}

function bounceFactory() {
	switch(config.transitionEaseDirection) {
		case "in": return d3.easeBounceIn;
		case "out": return d3.easeBounceOut;
		case "inout": return d3.easeBounceInOut;
		default: console.log("You done fucked up!");
	}
}
