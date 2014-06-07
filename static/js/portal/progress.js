var chart1;
$(document).ready(function () {
	if (data != null) {
		var options = {
			chart: {
				renderTo: 'placeholder',
			},
			colors: [
				'#772953',
				'#4572A7',
				'#AA4643',
				'#89A54E',
				'#80699B',
				'#3D96AE',
				'#DB843D',
				'#92A8CD',
				'#A47D7C',
				'#B5CA92'
			],
			title: {
				text: null
			},
			labels: {
				style: {
					color: '772953'
				}
			},
			xAxis: {
				title: {
					text: 'Dates',
					style: {
						color: '#772953'
					}
				},
				type: 'datetime',
			},
			yAxis: {
				title: {
					text: 'Notes',
					style: {
						color: '#772953'
					}
				}
			},
			tooltip: {
				formatter: function() {
					return '<b>'+ new Date(this.x).toGMTString()+'</b><br/>'+
						this.series.name + ': ' + this.y;
				}
			},
			legend: {
				enabled: false,
			},
			plotOptions: {
				series: {
					cursor: 'pointer',
					point: {
						events: {
							click: function() {

							}
						}
					},
					marker: {
						lineWidth: 1
					}
				}
			},
			series: [{
				name: 'Note',
			},]
		}
		options.series[0].data = data;
		chart1 = new Highcharts.Chart(options);
	}
});
