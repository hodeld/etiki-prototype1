/**
 * 
 */

// jquery
$(document).ready(
		function() {


			$("#id_sust_domain").change(function() { 
				load_tags();
			});

			$("#id_sust_tendency").change(function() { 
				load_tags();
			});
			
			
			$("#id_year").on(
					'dp.update',
					function(e) { // e = event

						var year_str = $(this).val();
						var date_str = '01.01.' + year_str;

						$('#id_date_published').data("DateTimePicker").clear();
						$('#id_date_published').data("DateTimePicker")
								.defaultDate(date_str);

					});
			$("#id_date_published").on(
					'dp.update',
					function(e) { // e = event
						set_firstjan(e, this);

					});
			$("#id_date_impact").on(
					'dp.update',
					function(e) { // e = event
						set_firstjan(e, this);

					});

		});

function set_firstjan(e, element) { // e = event
	
	var changed = e["change"];
	if (changed == 'YYYY'){ //if year changed
		var dt = e.viewDate._d;
		var year_i = dt.getFullYear() //integer
		if (e.viewDate._i) { //last date
			var m_str  = e.viewDate._i.substring(0,6);				
		}
		else {
			var m_str  = '01.01.';	
		}
		var date_str = m_str + year_i.toString();
		$(element).data("DateTimePicker").clear();
		$(element).data("DateTimePicker")
				.defaultDate(date_str);
	}
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