$(document).ready(function() {
	$('tbody').addClass("list"); // for list filter
	$('.table-container').attr('id', 'impev-list'); // for list filter


	$('.table-container').append('<input  class="search" placeholder="Search"  />');
	
	//needs to be inside ready, sothat elements of specific ID and Class
	var impevopts = {
			  valueNames: [ 'company', 'country' ]
			};

	var impevList = new List('impev-list', impevopts);


	
});


