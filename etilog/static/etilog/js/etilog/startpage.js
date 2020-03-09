/**
 * 
 */

// jquery
$(document).ready(function() {

	
	
	$(window).resize(function(){ //window changes-> a lot need to be handled
		var timeout = false, // holder for timeout id
	    delay = 400; // delay after event is "complete" to run callback	
		// clear the timeout
		clearTimeout(timeout);
		// start timing for event "completion"
		timeout = setTimeout(set_topheadaer, delay);
    });
	
	if (landing == false){
		startsettings();		
	}
	
	
});
function startsettings(){	
	var filterDict = JSON.parse(jsData.filter_dict); 
	setFilterVisually(filterDict);
	setData(jsData);
	toggle_filter();
	scrollToEle();

}

function startanimation(){
	$('.landing').removeClass('landing'); 
	// call once when page is initialized; table must be 				
	toggle_filter();
	scrollToEle();

	}	


function scrollToEle(eleId = '#tabContent'){
	let hi = $('#id_contsearch').outerHeight() ; //smaller than navbar id_navbar
	$([document.documentElement, document.body]).animate({
	    scrollTop: $(eleId).offset().top - hi 
	}, 2000);

	
}

function set_topheadaer(){
	let hi = $('#id_contsearch').outerHeight() - 4; //smaller than navbar id_navbar
	$('th').css({ top: hi }); 	
}
	
