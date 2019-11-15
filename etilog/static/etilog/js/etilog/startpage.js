/**
 * 
 */

// jquery
$(document).ready(function() {
	//$('#id_search').on('click', startanimation);
	$('.topic-link').on('click', startanimation);

	
});

function startanimation(){
	if ($('#id_oviewtable').css('display') == 'none'){
		$('#id_oviewtable').slideDown(); //duration
		$('.fullsite-wrapper').css('height', 'auto');
		$('.bottomleft').removeClass('bottomleft');
		$('.changepos').addClass('position-relative');
		
		
		
	}
	
}
	
