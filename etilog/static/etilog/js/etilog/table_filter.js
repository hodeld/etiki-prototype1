

$(document).ready(function() {
	$('tbody').addClass("list"); // for list filter
	$('.table-container').attr('id', 'impev-list'); // for list filter


	$('.table-container').prepend('<input  class="search form-control" placeholder="Search"  />');
	
	$('#button-id-datefilter').attr("aria-pressed", datef); //datef: true or false
	change_activ();
	$('#button-id-datefilter').click(filter_toggle);
	
	//$('#id_row_f_company').hide();
	//$('#id_row_f_freetext').hide();
	$('.row_tags_class').hide();
	$('.row_tags_class').prop("disabled", true);
	
	
	
	
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
	
	//initialize bloodhound
	var colors_suggestions = new Bloodhound({
		  datumTokenizer: Bloodhound.tokenizers.whitespace, 
		  queryTokenizer: Bloodhound.tokenizers.whitespace, 
		  local: ['Red','Blood Red','White','Blue','Yellow','Green','Black','Pink','Orange']
		});
	//initialize bloodhound
	var companies = new Bloodhound({
		  datumTokenizer: Bloodhound.tokenizers.whitespace, //obj.whitespace('name') -> data needs to be transformed
		  queryTokenizer: Bloodhound.tokenizers.whitespace, 
		  prefetch: {
			  url: companies_url, // url set in html
			  //cache: true // defaults to true -> for testing	        
		        }		  
		});
	//initialize bloodhound
	var countries = new Bloodhound({
		  datumTokenizer: Bloodhound.tokenizers.whitespace, //obj.whitespace('name') -> data needs to be transformed
		  queryTokenizer: Bloodhound.tokenizers.whitespace, 
		  prefetch: {
			  url: countries_url, // url set in html   
		        }		  
		});
	//initialize bloodhound
	var references = new Bloodhound({
		  datumTokenizer: Bloodhound.tokenizers.whitespace, //obj.whitespace('name') -> data needs to be transformed
		  queryTokenizer: Bloodhound.tokenizers.whitespace, 
		  prefetch: {
			  url: references_url, // url set in html        
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
		  templates: {
		    header: multitemplate_st + 'Companies' + multitemplate_et
		  }
		},
		{
		  name: 'countries',
		  source: countries,
		  templates: {
		    header: multitemplate_st + 'Countries' + multitemplate_et
		  }
		},
		{
		  name: 'references',
		  source: references,
		  templates: {
		    header: multitemplate_st + 'Where was it published' + multitemplate_et
		  }
		
		
		});
	
	$('#id_search').bind('typeahead:select', function(ev, suggestion) {
		  	var val_str = suggestion;
			if (val_str.length > 0 ) {
				var modname = ev.handleObj.handler.arguments[2]; 
				if (modname == 'companies'){
					var elt = $('#id_f_company');
					
					
				}
				else {
					var elt = $('#id_f_freetext');
					
				}
			elt.tagsinput('add', suggestion);	//adds tag
			//elt.show();
			//$('#div-id-freetext').hide();
			$('#id_row_f_company').show();
			//$('.bootstrap-tagsinput').show();
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

