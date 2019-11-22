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
				window.scrollTo(0, 0);
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
	$('img').hide() //hide img from html text

});

function next_ie(){
	window.location.href = next_id_url; //as user clicked on a link
}
	
function extract_text(ele){	
	var source_url = $("#id_source_url").val();
	var get_url = $(ele).attr("url-get"); // get
	
	$("#id_impev_msg").html('reads text from website …');
	window.scrollTo(0, 0);
	$.ajax({ // initialize an AJAX request
		url : get_url, // set the url of the request (= '')
		data : {
			// both can be null
			'sourceurl' : source_url
		},
		success : function(response) { // `data` is the return of the
			var msg = response.message;
			if (response.is_valid == "true") {
				var text_str = response.stext;				
				var stitle = response.stitle;
		        var sdate = response.sdate;
		        var shtml = response.shtml;
		        
		        $("#id_date_text").val(sdate); 
		        $("#id_article_text").html(text_str); 
		        $("#id_article_title").val(stitle);
		        $("#id_article_html").val(shtml);	        
		        $("#id_articleshow").html(shtml);
		        $('img').hide()
		        $("#id_url_link").html(source_url);
		        $("#id_url_link").attr("href", source_url)
		        $("#id_titleshow").html(stitle);
		        
			}	
			var parse_res = response.parse_res;
			$("#id_result_parse_html").val(parse_res);
			$("#id_impev_msg").html(msg);

		}

	});
	
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