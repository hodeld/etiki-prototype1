

//global functions which override each other
$(document).ready(function() {
	
	google.charts.load("current", {packages:["corechart"]});
    //google.charts.setOnLoadCallback(drawChart);
	$(window).resize(function(){
		drawcharts = true;
		drawCharts();
		});
	
	$('#tab2[data-toggle="tab"]').on('shown.bs.tab', function (e) {
		drawCharts();
		});
	



	
	
});

function drawCharts(){
	//if visible and new data
	if ($('#tab2').attr("aria-selected") === "true" && drawcharts) {
		drawcharts = false;
		comp_ratings.forEach(function (item, index) {
			drawChart(item);
		});
	}	
}

function drawChart(co) {
	var etiki_colors = get_colors();
	var eleId = 'company-chart-' + co.pk;
	var ele = document.getElementById(eleId);
	
	
    var chartdata = google.visualization.arrayToDataTable([
    	 ['Tendency', 'Events'],
         ['Positive',     Number(co.num_pos)],
         ['Controversial', Number(co.num_con)],
         ['Negative', Number(co.num_neg)],
    ]);

    var chartoptions = {
      pieHole: 0.4,
      backgroundColor: 'transparent',
      legend: {position: 'none' },
      title: {position: 'none' },
      colors: etiki_colors, 
      chartArea: {'height': '100%'},
    };

    var chart = new google.visualization.PieChart(ele);
    chart.draw(chartdata, chartoptions);
  }
	
	
function size_ratings(ie_id) {
	var parId = '#company-chart '; //ie_id
	var fullwid = $(parId).width();
	var pos_num = Number(comp_details[ie_id][0]);
	var neg_num = Number(comp_details[ie_id][1]);
	var con_num = Number(comp_details[ie_id][2]);
	var tot_num = pos_num + neg_num + con_num;
	if (tot_num == 0){
		return
	}
	
	var pos_prz = pos_num/tot_num*100;
	var neg_prz = neg_num/tot_num*100;
	var con_prz = con_num/tot_num*100;
	
	$(parId+ '.div-img-pos').width(pos_prz + '%');
	$(parId+ '.div-img-neg').width(neg_prz + '%');
	$(parId+ '.div-img-con').width(con_prz + '%');
	
	$(parId+ '.text-pos').html(pos_num);
	$(parId+ '.text-neg').html(neg_num);
	$(parId+ '.text-con').html(con_num);
	
	
}

function get_colors(){
	var ele = document.getElementById('tabContent'); //any element
	
	var posCol = getComputedStyle(ele).getPropertyValue("--positive");
	var conCol = getComputedStyle(ele).getPropertyValue("--controversial");
	var negCol = getComputedStyle(ele).getPropertyValue("--negative");
	var colProps = [posCol, conCol, negCol]
	var cols =  []
	colProps.forEach(function(col){
		cols.push(col.trim()); col.trim(); //returns without whitespace

	});
	return cols
	
}

function imgError(ele){
	$(ele).hide();
	var altId = $(ele).attr('altid');
	$('#'+altId).css('visibility', 'visible');
	$('#'+altId).css('opacity', '1');
}

function showMockup(event){
	var target = $( event.target );
	if ( target.is( "path" ) || target.is( "a" ) ) {
		return false;
	}
	else {
		$('#wordcloud-tab').tab('show');
	}	
}
