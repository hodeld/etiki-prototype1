/**
 * 
 */

// jquery
$(document).ready(function() {
	//$('#id_search').on('click', startanimation);
	$('.topic-link').on('click', startanimation);
	
	//add class to change background
	//TODO use waypoints in future, also for background at top which will be behind thead
	$(window).scroll(function () {
		if ($(document).scrollTop() > 100) {
	        $('#id_contsearch').addClass("scrolled");
	        $('#small_logo').addClass("d-md-block") //only on large displays shown
	    } else {
	        $('#id_contsearch').removeClass("scrolled");
	        $('#small_logo').removeClass("d-md-block")
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

	
});

function startanimation(){
	if ($('#id_oviewtable').css('display') == 'none'){
		$('#id_oviewtable').slideDown(); //duration
		$('.fullsite-wrapper').css('height', 'auto');
		$('.bottomleft').removeClass('bottomleft');
		$('.changepos').addClass('position-relative');
		// call once when page is initialized; table must be 
		set_topheadaer()
		
	}	
}
function set_topheadaer(){
	let hi = $('#id_contsearch').outerHeight() - 2; //smaller than navbar id_navbar
	$('th').css({ top: hi }); 	
}
	
