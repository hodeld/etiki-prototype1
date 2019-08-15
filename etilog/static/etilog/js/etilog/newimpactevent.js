/**
 * 
 */

// jquery

$(document).ready(function() {

	$("#id_btn_company").click( function() { 
		var url = $(this).attr("admin-add-url");
		w = window.open(url, "id_company", "width=600, height=800, scrollbars=yes");
		
		//var win = window.open(url, "popupWindow", "width=600, height=800, scrollbars=yes");
		//win.focus();
        //return false;
			
		
		

	});

	$("#id_sust_domain").change(function() { // jquery code $# -> gives ide; if radioselect: id_id_sust_domain_0_2
		var url = $("#id_sust_category").attr("data-susts-url"); // get the url of

		var domainId = $(this).val(); // get the selected Domain ID from the
										// HTML input
		// var cachname = $("#dateForm").attr("cachname_tbldict");
		$.ajax({ // initialize an AJAX request
			url : url, // set the url of the request (= '')
			data : {
				'domainId' : domainId
			// add the domainId to the GET parameters
			},
			success: function (data) {   // `data` is the return of the `load_susts` view function
		          $("#id_sust_category").html(data);  // replace the contents of the sust input with the data that came from the server
		        }

		});
	});
	
	$("#id_year").on('dp.update', function(e) { // e = event

		var year_str = $(this).val();
		var date_str = '01.01.' + year_str;

		$('#id_date_published').data("DateTimePicker").defaultDate(date_str);

	});

});
