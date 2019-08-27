$(document).ready(function() {
	$('tbody').addClass("list"); // for list filter
	$('.table-container').attr('id', 'impev-list'); // for list filter


	$('.table-container').prepend('<input  class="search form-control" placeholder="Search"  />');
	
	//needs to be inside ready, sothat elements of specific ID and Class
	var impevopts = {
			  valueNames: [ 'company', 'country', 'reference', 'sust_category', 'date_published' ],
			  page: 20,
			  pagination: {
			    innerWindow: 2,
			    outerWindow: 1,
			    left: 0,
			    right: 0,
			    paginationClass: "pagination",
			    }
			};

	var impevList = new List('impev-list', impevopts);


	
});


