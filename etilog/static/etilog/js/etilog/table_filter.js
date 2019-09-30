

$(document).ready(function() {
	
	//button select for categories
	$('.btnselect').on('click', set_val_from_btn);
	set_filterbtns();
	
	//$('.row_tags_class').hide(); -> done in css
	
	//add tagsinput on hidden fields
	$('.f_tagsinput').tagsinput({
		  	itemValue: 'id',
			itemText: 'name',
		});
	
	//form ajax options
	var options = {			
			  success: function(data) {
			    $("#id_ovtable").html(data);
			    prepare_list()
			  }
			};
	// pass options to ajaxForm
	$('#id_filterform').ajaxForm(options);
	
	

    var timeout = false, // holder for timeout id
	    delay = 400; // delay after event is "complete" to run callback
    
    // call once when page is initialized
	set_topheadaer()
	
	// call once to initialize page
	$(window).resize(function(){ //window changes-> a lot need to be handled
		// clear the timeout
		clearTimeout(timeout);
		// start timing for event "completion"
		timeout = setTimeout(set_topheadaer, delay);
    });
	
	//directly submit on filterinputs:
	$('.f_input').change(function(ev){
		var foid = '#' + ev.target.form.id;
		$(foid).submit();		
		
	});
	
	//directly submit on datetimeinput
	$(".dateyearpicker").on('dp.change', function(ev) { // e = event
		var foid = '#' + ev.target.form.id;
		$(foid).submit();

	});

	
	//initialize bloodhound
	var companies = new Bloodhound({
		  datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'), //obj.whitespace('name') -> data needs to be transformed
		  queryTokenizer: Bloodhound.tokenizers.whitespace, 
		  prefetch: {
			  url: companies_url, // url set in html
			  cache: false // defaults to true -> for testing	        
		        }		  
		});
	//initialize bloodhound
	var countries = new Bloodhound({
		  datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),//obj.whitespace('name') -> data needs to be transformed
		  queryTokenizer: Bloodhound.tokenizers.whitespace, 
		  prefetch: {
			  url: countries_url, // url set in html   
			  cache: false // 
		        }		  
		});
	//initialize bloodhound
	var references = new Bloodhound({
		  datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'), //obj.whitespace('name') -> data needs to be transformed
		  queryTokenizer: Bloodhound.tokenizers.whitespace, 
		  prefetch: {
			  url: references_url, // url set in html  
			  cache: false // 
		        }		  
		});
	var elttag = $('.f_tagsinput') //array of elements
	
	var multitemplate_st = '<h5 class="category-name text-primary">';
	var multitemplate_et = '</h5>';
	
	//initialize typehead -> needs to be below source (assignment is in order in js!
	$('#id_search').typeahead(
		{
			highlight: true
		},
		{
		  name: 'companies',
		  source: companies,
		  display: 'name',
		  templates: {
		    header: multitemplate_st + 'Companies' + multitemplate_et
		  }
		},
		{
		  name: 'countries',
		  source: countries,
		  display: 'name',
		  templates: {
		    header: multitemplate_st + 'Countries' + multitemplate_et
		  }
		},
		{
		  name: 'references',
		  source: references,
		  display: 'name',
		  templates: {
		    header: multitemplate_st + 'Where was it published' + multitemplate_et
		  }
		
		
		});

	$('#id_search').bind('typeahead:select', function(ev, suggestion) {
		  	//var val_str = suggestion;
		  	var val_str = suggestion['name'];
		  	var val_id = suggestion['id'];
		  	
			
		  	if (val_str.length > 0 ) {
				var modname = ev.handleObj.handler.arguments[2]; 
				if (modname == 'companies'){
					var elt = $('#id_f_company');
					var el_id = '#id_row_f_company';
				}
				else if (modname == 'countries'){
					var elt = $('#id_f_country');
					var el_id = '#id_row_f_country';					
				}
				else if (modname == 'references'){
					var elt = $('#id_f_reference');
					var el_id = '#id_row_f_reference';					
				}					
				
				else {
					var elt = $('#id_f_freetext');					
				}
		    
				elt.tagsinput('add', suggestion);	//adds tag	
				
				$(el_id).show();
				$(this).typeahead('val', ''); //typeahead input			
			}
			
		
	});
	// if changed without suggestion
	$('#id_search').bind('typeahead:change', function() {
		var val_str = $(this).typeahead('val');
		var elt = $('#id_f_freetext');
		
		elt.tagsinput('add', val_str);	//adds tag
		$('#id_row_f_freetext').show();
		//$(this).val(''); 
		$(this).typeahead('val', ''); //typeahead input
		
		
	});
     //for List.js
     prepare_list()

});



function set_val_from_btn(event) {
	var el_id = '#' + event.target.id;
	var id_val = Number(event.target.name);
	var input_id = '#' + $(event.target).attr('targfield');
	var pressed = event.target.attributes['aria-pressed'].value; // true or false
	//var el_val = $('#id_sust_domain').val();
	var el_val = $(input_id).val();
	var val_list = JSON.parse("[" + el_val + "]"); 
	//var val_list = el_val.split();

	if (pressed  == "false"){ //means was pressed now
		

		val_list.push(id_val)
		
	}
	else{

		var index = val_list.indexOf(id_val);
		if (index > -1) {
			val_list.splice(index, 1);
		    }
	}
	

	$(input_id).val(val_list)
				.trigger('change'); //needed for hidden input fields
}

function prepare_list(){
	$('tbody').addClass("list"); // for list filter
 	$('.table-container').attr('id', 'impev-list'); // for list filter
 	//need to be in same container as table for list filter
 	//$('.table-container').prepend('<input  class="search form-control" placeholder="Search"  />');
 	
 	$('.table-container').append('<nav aria-label="Table navigation"><ul class="pagination justify-content-center"></ul></nav>')
 	
 	var impevopts = {
 			  valueNames: [ 'company', 'country', 'reference', 'sust_domain', 'topics',
 				  'date_published', 'date_sort', 'reference_sort', 'sudom_sort'],
 			  page: 20,
 			  pagination: {
 			    innerWindow: 2,
 			    outerWindow: 1,
 			    left: 0,
 			    right: 0,
 			    paginationClass: "pagination", //class name generated in django-table
 			    }
 			};

 	//initiate List incl. pagination
 	var impevList = new List('impev-list', impevopts);
 	//searchfield outside container:
 	$('#id_search').on('keyup', function() {
 		  var searchString = $(this).val();
 		 impevList.search(searchString);
 		});
 	$('#id_search').bind('typeahead:select', function() {
 		impevList.search(''); //to clear List search 		
 	}); 	
}
function set_topheadaer(){
	let hi = $('#id_navbar').outerHeight() - 2; //smaller than navbar
	$('th').css({ top: hi }); 	
}

//not used at the moment
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


function set_filtertags(){
	$.each(tags_dict, function( k, v ) {
		var el_id = '#id_f_'+ k;	
		var el_row_id = '#id_row_f_' + k;
		$.each(v, function(ki, vi){
			$(el_id).tagsinput('add', vi);
			});

	
		$(el_row_id).show();
	});	
}
function set_filterbtns(){
	$.each(btns_dict, function( k, v ) {
		var part_id = '#id-' + k + '-btn-';	//k = sust_domain or sust_tendency
		$.each(v, function(index, val_i){
			var btn_id = part_id + val_i;
			//$(btn_id).addClass("active");
			$(btn_id).click(); //clicks and adds to hidden input
			});
	});	
}