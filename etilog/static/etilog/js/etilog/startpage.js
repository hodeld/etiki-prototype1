/**
 * 
 */

// jquery
$(document).ready(function() {

	//add class to change background
	//TODO use waypoints in future, also for background at top which will be behind thead
	$(window).scroll(function () {
		var cssclass = "d-block"; //"d-md-block";
		if ($(document).scrollTop() > 100) {			
	        $('#id_contsearch').addClass("scrolled");
	        $('.fullscreen-wrapper').addClass("scrolled");
	        $('#small_logo').addClass(cssclass) //only on large displays shown
	    } else {
	    	$('#id_contsearch').removeClass("scrolled");
	        $('.fullscreen-wrapper').removeClass("scrolled");
	        $('#small_logo').removeClass(cssclass);
	    }
	});
	
	
	
	$(window).resize(function(){ //window changes-> a lot need to be handled
		var timeout = false, // holder for timeout id
	    delay = 400; // delay after event is "complete" to run callback	
		// clear the timeout
		clearTimeout(timeout);
		// start timing for event "completion"
		timeout = setTimeout(set_topheadaer, delay);
    });
	
	startsettings();
	
});
function startsettings(){
	if (showpage == 'True'){
		var filterDict = JSON.parse(jsData.filter_dict); 
		setFilterVisually(filterDict);
		setData(jsData);
		showElements();
		
	}	
}
function showElements(){
	var ele = $('#tabContent');
	//$('#link_filter').show();
	$('#div_filterform').addClass('show');
	$('.fullsite-wrapper-start').removeClass('fullsite-wrapper-start');
	$('.bottomleft').removeClass('bottomleft');
	$('.changepos').addClass('position-relative');
	ele.show(); 
	// call once when page is initialized; table must be 				
	toggle_filter();
	scrollToEle();
	
}	


function startanimation(){
	var ele = $('#tabContent');
	if (ele.css('display') == 'none'){
		//before table has data:
		$('#div_filterform').addClass('show');

		$('.fullsite-wrapper-start').removeClass('fullsite-wrapper-start');
		$('.bottomleft').removeClass('bottomleft');
		$('.changepos').addClass('position-relative');
		ele.show(); 
		// call once when page is initialized; table must be 				
		toggle_filter();
		scrollToEle();

	}	
}


function scrollToEle(eleId = '#id_oviewtable'){
	let hi = $('#id_contsearch').outerHeight() ; //smaller than navbar id_navbar
	$([document.documentElement, document.body]).animate({
	    scrollTop: $(eleId).offset().top - hi 
	}, 2000);

	
}

function set_topheadaer(){
	let hi = $('#id_contsearch').outerHeight() - 4; //smaller than navbar id_navbar
	$('th').css({ top: hi }); 	
}
	
