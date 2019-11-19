/**
 * 
 */

// jquery
$(document).ready(function() {
	//$('#id_search').on('click', startanimation);
	$('.topic-link').on('click', startanimation);
	
	//add class to change background
	$(window).scroll(function () {
		if ($(document).scrollTop() > 50) {
	        $('#id_contsearch').addClass("scrolled");
	    } else {
	        $('#id_contsearch').removeClass("scrolled");
	    }
	});

	
});

function startanimation(){
	if ($('#id_oviewtable').css('display') == 'none'){
		$('#id_oviewtable').slideDown(); //duration
		$('.fullsite-wrapper').css('height', 'auto');
		$('.bottomleft').removeClass('bottomleft');
		$('.changepos').addClass('position-relative');
		
		
		
	}
	
}
	
