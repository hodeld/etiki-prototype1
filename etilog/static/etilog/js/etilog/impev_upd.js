/**
 * 
 */

// jquery
$(document).ready(function() {

	// form ajax options
	var formoptions = {
		success : function(response) {
			var msg = response.message;
			if (response.is_valid == "false") {
				//$("#id_impev_msg").html(JSON.stringify(msg));
				$("#id_impev_msg").html(msg);
				var error_items = response.err_items ;
				error_items.forEach(function (item, index) {
					var el_id = '#id_' + item;
					$(el_id).addClass('is-invalid') //django class
					}); 
				//$("#id_impevform").html(response.form); // to show errors
			}
			else {
				$("#id_impev_msg").html(msg);
				$('.is-invalid').removeClass('is-invalid') //django class
			}
		}
	
	};
	// pass options to ajaxForm
	$('#id_impevform').ajaxForm(formoptions);
	
	

	$("#id_sust_domain").change(function() {
		load_tags();
	});

	$("#id_sust_tendency").change(function() {
		load_tags();
	});

	$("#id_year").on('dp.update', function(e) { // e = event

		var year_str = $(this).val();
		var date_str = '01.01.' + year_str;

		$('#id_date_published').data("DateTimePicker").clear();
		$('#id_date_published').data("DateTimePicker").defaultDate(date_str);

	});

});

function next_ie(){
	window.location.href = next_id_url; //as user clicked on a link
}
	

function load_tags(){
	var url = $("#id_sust_tags").attr("data-url"); // get
	// the
	// url
	// of

	var domainId = $("#id_sust_domain").val(); // get the selected Domain ID
	var categoryId = $("#id_sust_tendency").val(); // get the selected tendency ID
	// from the
	// HTML input
	// var cachname = $("#dateForm").attr("cachname_tbldict");
	$.ajax({ // initialize an AJAX request
		url : url, // set the url of the request (= '')
		data : {
			// both can be null
			'domainId' : domainId,
			'categoryId' : categoryId
			
		// add the domainId to the GET parameters
		},
		success : function(data) { // `data` is the return of the
		// `load_susts` view function
			$("#id_sust_tags").html(data); // replace the
			// contents of the
			// sust input with
			// the data that
			// came from the
			// server
		}

	});
	
}