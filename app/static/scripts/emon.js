$.fn.drawchart7=function(){
	var dts01=new Array();
	var dts03=new Array();
	$('table').find('.data-year').each(function(){
		var y=parseInt($(this).find('.yyyy').text());
		var m=parseInt($(this).find('.mm').text())-1;
		var d=parseInt($(this).find('.dd').text());
		var v01=parseFloat($(this).find('.val01').text());
		var v03=parseFloat($(this).find('.val03').text());
		dts01.push([Date.UTC(y,m,d),v01]);
		dts03.push([Date.UTC(y,m,d),v03]);
	});
	var yearstr=$('.yearstr').text();
	var options={
		chart:{
			type:'area'
		},
		title:{
			text: yearstr+'年分类型用电量'
		},
		xAxis:{
			type:'datetime',
			title:{
				text:null
			}
		},
		yAxis:{
			title:{
				text:'用电量（千瓦时）'
			},
			min:0
		},
		plotOptions:{
			area:{
				stacking:'normal'
			}
		},
		tooltip:{
			split:true,
			valueSuffix:' 千瓦时'
		},
		series:[{
			name:'中央空调',
			data: dts03,
			color:'#fa6'
		},{
			name:'日常用电',
			data: dts01,
			color:'#8df'
		}]
	};
	var chart = Highcharts.chart('container7', options);
}

/*$.fn.drawchart1=function(){
	//var dts01=new Array();
	//var dts03=new Array();
	var dts=new Array();
	$('table').find('.data-year').each(function(){
		var y=parseInt($(this).find('.yyyy').text());
		var m=parseInt($(this).find('.mm').text())-1;
		var d=parseInt($(this).find('.dd').text());
		//var v01=parseFloat($(this).find('.val01').text());
		//var v03=parseFloat($(this).find('.val03').text());
		var vtotal=parseFloat($(this).find('.valtotal').text());
		//dts01.push([Date.UTC(y,m,d),v01]);
		//dts03.push([Date.UTC(y,m,d),v03]);
		dts.push([Date.UTC(y,m,d),vtotal]);
	});
	var options={
		chart: {
			type: 'area'
			//zoomType:'x'
		},
		title: {
			text: '综合楼用电量变化'
		},
		xAxis: {
			type: 'datetime',
			title: {
				text: null
			}
		},
		colors: ['#6CF', '#39F', '#06C', '#036', '#000'],
		yAxis: {
			title: {
				text: '用电量（千瓦时）'
			},
			min: 0
		},
		tooltip: {
			headerFormat: '<b>{series.name}</b><br>',
			pointFormat: '{point.x:%e. %b}: {point.y:.2f} m'
		},
		plotOptions: {
	            area: {
        	        fillColor: {
                	    linearGradient: {
                        	x1: 0,
	                        y1: 0,
        	                x2: 0,
                	        y2: 1
	                    },
        	            stops: [
                	        [0, Highcharts.getOptions().colors[0]],
                        	[200000, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
	                    ]
        	        },
                	marker: {
	                    radius: 2
        	        },
                	lineWidth: 1,
	                states: {
        	            hover: {
                	        lineWidth: 1
	                    }
        	        },
                	threshold: null
	            }
        	},
		series: [{
			name: '用电量',
		// Define the data points. All series have a dummy year
		// of 1970/71 in order to be compared on the same x axis. Note
		// that in JavaScript, months start at 0 for January, 1 for February etc.
			data: dts,
		}]
	};
	var chart = Highcharts.chart('container1', options);
}
*/

$.fn.drawchart2=function(){
	var dts=new Array();
	var xs=new Array();
	var ys=new Array();
	$('table').find('.data-hp').each(function(){
		var x=parseInt($(this).find('.xval').text())-1;
		var y=parseInt($(this).find('.yval').text());
		var v=parseFloat($(this).find('.val').text());
		dts.push([x,y,v]);
	});
	$('.mdata-hours').find('.m-hour').each(function(){
		var m_h=$(this).text();
		ys.push(m_h);
	});
	$('.mdata-days').find('.m-day').each(function(){
		var m_d=$(this).text();
		xs.push(m_d);
	});
	var m_year=$('.m_year').text();
	var m_month=$('.m_month').text();
	var options={
		chart:{
			type: 'heatmap',
			//marginTop: 40,
			marginBottom: 80,
			plotBorderWidth: 1
		},
		title: {
			text: m_year+'年'+m_month+'月用电量'
		},
		xAxis: {
			categories: xs,
			title: {
				text: '日期'
			}
		},
		yAxis: {
			categories: ys,
			title: {
				text: '每日时间段'
			}
		},
		colorAxis: {
			stops: [
				[0, '#3060cf'],
				[0.5, '#fffbbc'],
				[0.9, '#c4463a']
			],
			min: 0
		},
		legend: {
			align: 'right',
			layout: 'vertical',
			margin: 0,
			verticalAlign: 'top',
			y: 24,
			symbolHeight: 280
		},
		tooltip: {
			formatter: function () {
				return '<b>'+m_year+'-'+m_month+'-' + this.series.xAxis.categories[this.point.x] + ' ' + this.series.yAxis.categories[this.point.y] + ' 用电量 ' +this.point.value + ' 千瓦时</b>';
			}
		},
		series: [{
			name: '8月份用电量',
			borderWidth: 0,
			data: dts
		}]
	};
	var chart = Highcharts.chart('container2', options);
}

$.fn.drawchart3=function(){
	var dts=new Array();
	var realval=parseInt($('.realval').text());
	dts.push(realval);
	var options={
		chart: {
			type: 'solidgauge',
			height:308
			},
		title: {
			text: '今日实时用电量'
			},
    		pane: {
        		center: ['50%', '85%'],
        		size: '140%',
		        startAngle: -90,
		        endAngle: 90,
		        background: {
				backgroundColor: (Highcharts.theme && Highcharts.theme.background2) || '#EEE',
            			innerRadius: '60%',
            			outerRadius: '100%',
            			shape: 'arc'
        			}
    			},
    		yAxis: {
        		stops: [
            			[0.1, '#55BF3B'], // green
            			[0.5, '#DDDF0D'], // yellow
            			[0.9, '#DF5353'] // red
        		],
        		lineWidth: 0,
        		minorTickInterval: null,
        		tickInterval: 2500,
        		tickWidth: 0,
        		title: null,
        		labels: {
            			y: 16
        		},
        		min: 0,
        		max: 2500
    		},
    		plotOptions: {
        		solidgauge: {
            			dataLabels: {
                			y: 5,
                			borderWidth: 0,
                			useHTML: true
            			}	
        		}
    		},
		credits: {
        		enabled: false
    		},
    		series: [{
        		data: dts,
        		dataLabels: {
            			format: '<div style="text-align:center"><span style="font-size:32px;color:' +
            			((Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black') + '">{y}</span><br/>' +
            			'<span style="font-size:12px;color:silver">千瓦时</span></div>'
        		}
    		}]
	};
	var chart = Highcharts.chart('container3', options);
}

$.fn.drawchart4=function(){
	var ds=new Array();
	var tvs=new Array();
	var lvs=new Array();
	$('table').find('.data-mdts').each(function(){
		var d=$(this).find('.dd').text();
		ds.push(d);
		var tv=parseInt($(this).find('.tval').text());
		tvs.push(tv);
		var lv=parseInt($(this).find('.lval').text());
		lvs.push(lv);
	});
	var options={
		chart:{
			type:'column'
		},
		title:{
			text:'本月用电量与去年同期对比'
		},
		xAxis:{
			categories: ds,
			crosshair:true
		},
		yAxis:{
			min: 0,
			title: {
				text: '用电量（千瓦时）'
			}
		},
		tooltip:{
			headerFormat: '<span style="font-size:10px">{point.key}日用电量</span><table>',
			pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
            			'<td style="padding:0"><b>{point.y:.1f} 千瓦时</b></td></tr>',
			footerFormat: '</table>',
			shared: true,
			useHTML: true
		},
		plotOptions: {
			column: {
				pointPadding: 0.2,
				borderWidth: 0
			}
		},
		series:[{
			name: '本月',
			data: tvs,
			color:'#dd8833'
		},{
			name: '去年同期',
			data: lvs,
			color:'#aaaacc'
		}]
	};
	var chart = Highcharts.chart('container4', options);
}
	
$.fn.drawchart5=function(){
	var flrs=new Array();
	var vals=new Array();
	$('table').find('.data-tdvs').each(function(){
		var flr=$(this).find('.flr').text();
		flrs.push(flr);
		var val=parseFloat($(this).find('.val').text());
		vals.push(val);
	});
	var options={
		chart:{
			type: 'bar',
			height:800
		},
		title:{
			text: '各楼层实时用电量'
		},
		xAxis:{
			categories:flrs,
			title:{
				text:'楼层'
			}
		},
		yAxis:{
			min:0,
			title:{
				text:'用电量（千瓦时）',
				align:'high'
			},
			labels:{
				overflow:'justify'
			}
		},
		tooltip:{
			valueSuffix:'千瓦时'
		},
		plotOptions:{
			bar:{
				dataLabels:{
					enabled:true
				}
			}
		},
		series:[{
			name:'今日实时用电量',
			data:vals
		}]
	};
	var chart=Highcharts.chart('container5',options);
}

$.fn.drawchart6=function(){
	var dts=new Array();
	$('table').find('.data-pie').each(function(){
		var name=$(this).find('.name').text();
		var val=parseFloat($(this).find('.val').text());
		dts.push([name,val]);
	});
	var options={
		chart:{
			type:'pie',
			height:450,
			options3d:{
				enabled:true,
				alpha:45,
				beta:0,
				depth:35
			}
		},
		title:{
			text:'各类用电实时占比'
		},
		plotOptions:{
			pie:{
				allowPointSelect:true,
				cursor:'pointer',
				depth:35,
				dataLabels:{
					enabled:true,
                			format: '<b>{point.name}</b>: {point.percentage:.1f} %'
				}
			}
		},
		series:[{
			name: '今日用电量',
			type: 'pie',
			data: dts
		}]
	};
	var chart=Highcharts.chart('container6',options);
}

	

function myTimer(){
	var datatime=$('.datatime').text();
	var floornumber=$('.floornumber').text();
	$.post('realdataquery',{
		datatime:datatime,
		floornumber:floornumber
	},function(result){
		if(result!='NULL'){
			$('#realdataframe').text("");
			$('#realdataframe').append(result);
			var datatime=$('.datatime').text();
			$('#datatime').text(datatime);
			$('#container3').drawchart3();
			$('#container4').drawchart4();
			$('#container5').drawchart5();
			$('#container6').drawchart6();
		}
	});
}

$(document).ready(function(){
	var datatime=$('.datatime').text();
	$('#datatime').text(datatime);
	//$('#container1').drawchart1();
	$('#container7').drawchart7();
	$('#container2').drawchart2();
	$('#container3').drawchart3();
	$('#container4').drawchart4();
	$('#container5').drawchart5();
	$('#container6').drawchart6();

	$('#yearquery').click(function(){
		var year=$('#y_yearvalue').val();
		$.post('yearquery',{
			year:year
		},
		function(result){
				$('#yeardataframe').text("");
				$('#yeardataframe').append(result);
				$('#container7').drawchart7();
		});
	});

	$('#monthquery').click(function(){
		var year=$('#m_yearvalue').val();
		var month=$('#m_monthvalue').val();
		$.post('monthquery',{
			year:year,
			month:month
		},
		function(result){
				$('#monthdataframe').text("");
				$('#monthdataframe').append(result);
				$('#container2').drawchart2();
		});
	});


	var myVar=setInterval(myTimer,60000);
});
