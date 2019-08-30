$(document).ready(function() {
	$('tbody').addClass("list"); // for list filter
	$('.table-container').attr('id', 'impev-list'); // for list filter


	$('.table-container').prepend('<input  class="search form-control" placeholder="Search"  />');
	
	$('#button-id-datefilter').attr("aria-pressed", datef); //datef: true or false
	change_activ();
	$('#button-id-datefilter').click(filter_toggle);
	
	//needs to be inside ready, sothat elements of specific ID and Class
	var impevopts = {
			  valueNames: [ 'company', 'country', 'reference', 'sust_category', 'date_published' ],
			  page: 20,
			  pagination: {
			    innerWindow: 2,
			    outerWindow: 1,
			    left: 0,
			    right: 0,
			    paginationClass: "pagination", //class name generated in django-table
			    }
			};

	var impevList = new List('impev-list', impevopts);


	
});

function filter_toggle(event) {
	var filter = event.target.name;
	var oform = event.target.form;
	var pressed = event.target.attributes['aria-pressed'].value; // true or false
	var input = document.createElement("input");
	var inputname =  'i-' + filter
	var inputid =  'id-i-' + filter
	var filterinput =  document.getElementsByName(inputname)[0]; //ElementS for Name -> then a list
	if (filterinput  == null){
		
		
		var filterinput = document.createElement("input");
		filterinput.setAttribute("type", "hidden");
		filterinput.setAttribute("id", inputid);
		filterinput.setAttribute("name", inputname);
	}
	var val = "true";
	if (pressed  == "true"){
		val = "false"
	}
	filterinput.value = val;
	//oform.appendChild(filterinput); //appends hidden input field; send request directly did not get response?!
	//oform.submit();
}
function change_activ(){
	if (datef == true){
		$('#button-id-datefilter').addClass("active");
	}
	else {
		return  $('#button-id-datefilter').removeClass("active");
	
	}	
}
