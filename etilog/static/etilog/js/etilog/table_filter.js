

$(document).ready(function() {
	$('tbody').addClass("list"); // for list filter
	$('.table-container').attr('id', 'impev-list'); // for list filter


	$('.table-container').prepend('<input  class="search form-control" placeholder="Search"  />');
	
	$('#button-id-datefilter').attr("aria-pressed", datef); //datef: true or false
	change_activ();
	$('#button-id-datefilter').click(filter_toggle);
	
	//$('.row_tags_class').hide(); -> done in css
	
	$('#id_filterform').submit(function() {
		  $('.f_tagsinput').prop("disabled", false);
		});
	$('.f_tagsinput').tagsinput({
		  	itemValue: 'id',
		  	
		  	//itemValue: 'jsobj',
		  	//itemValue: 'name',
			//itemValue: function(item) {
				//var val_id = item.id;
		//var val_name = item.name;
		//var valobj = {[val_id]: val_name};
		//var jsobj = JSON.stringify(valobj);
		//return jsobj;
		//},
			
			itemText: 'name',
		});
	
	
	set_filtertags();
	
	
	
	//initialize bloodhound
	var colors_suggestions = new Bloodhound({
		  datumTokenizer: Bloodhound.tokenizers.whitespace, 
		  queryTokenizer: Bloodhound.tokenizers.whitespace, 
		  local: ['Red','Blood Red','White','Blue','Yellow','Green','Black','Pink','Orange']
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
	
	$.each(elttag, function( index, elt ) {
		val_str = $(elt).val();
		if (val_str){
			val_list = val_str.split(",");
			val_list.forEach(function (val_id, index) {
				if (typeof(suggestion_dict) !== 'undefined'){
					modname = 'companies'
					sugg_list = suggestion_dict[modname];
					suggestion = sugg_list[val_id];
					elt.tagsinput('add', suggestion);
					$(el_id).show();				  
					}
		})
		}
	});
	
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

	var suggestion_dict = {
			'companies':{},
			'countries':{},
			'references':{}						
	};	
	
		
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
				
				//var val_id = suggestion.id;
				//var val_name = suggestion.name;
				
			    var valobj = {[val_id]: val_str};
			    var jsobj = JSON.stringify(valobj);
			    //suggestion['jsobj'] = jsobj;
			    //suggestion['jsobj'] = '{"name":"John","age":30,"city":"New York"}'
			    
				elt.tagsinput('add', suggestion);	//adds tag
				
				
				$('#id_f_company_array').val(jsobj);
				
				
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
	
	

     
     $('#id_searchtags').tagsinput({ //options only when without data_role
		typeaheadjs: 
		(
				//Configuration options
				{
			  hint: true,
			  highlight: true,
			  minLength: 1
			},
		//data options: mandatory
			{
        source: colors_suggestions
        })
		
       
     });
   //needs to be inside ready, sothat elements of specific ID and Class
     // at the end as if no pages -> error
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

function set_filtertags(){
	$.each(tags_dict, function( k, v ) {
		var el_id = '#id_f_'+ k;	
		var el_row_id = '#id_row_f_' + k;
		$.each(v, function(ki, vi){
			$(el_id).tagsinput('add', vi);
			});
		//$(el_id).tagsinput('add', v);	//adds tag
	
		$(el_row_id).show();
	});	
}

