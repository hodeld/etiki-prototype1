

$(document).ready(function() {
	//button select for categories
	$('.btnselect').on('click', set_val_from_btn);
	
	$('#link_filter').click(function() {
		toggle_filter()
	});
	$('#filterClose').click(function() {
		toggle_filter()
	});
	$('#filterClear').click(function() {
		clearFilter()
	});
	
	
	//$('.row_tags_class').hide(); -> done in css
	
	//add tagsinput on hidden fields
	$('.f_tagsinput').tagsinput({
		  	itemValue: 'id',
			itemText: 'name',
			
		});
	$('.f_tagsinput').on('itemRemoved', function(event) {
		if ($(this).tagsinput('items').length == 0 ){
			var modname = $(this).attr('name');
			var el_id = '#id_row_f_' + modname;
			$(el_id).hide();				
		}

		});
	
	//form ajax options
	var options = {		
			
			beforeSubmit: function() {
					$("#id_message").html('calculating results …');
					setFilterIcon();
					if (landing  == true){ //means was pressed now
						startanimation(); // only first time when table is hidden						
					}
				
					var acturl = $('#id_filterform').serialize(); //
					var searchurl = list_url +  'search?' + acturl; //list_url: etilog:home
					window.history.pushState("", "", searchurl); //TODO direct url search
			},
			success : function(response) {
				setData(response)
					
				},
			url: list_url, //needed to be defined due to searchurl
			};
	// pass options to ajaxForm
	$('#id_filterform').ajaxForm(options);
	
	

    
	
	//directly submit on filterinputs:
	$('.f_input').change(function(ev){
		submitFilterForm(ev)
	});
	
	//directly submit on datetimeinput
	$(".dateyearpicker").on('dp.change', function(ev) { // e = event
		submitFilterForm(ev)
	});

	
	
	
	var elttag = $('.f_tagsinput') //array of elements
	
	var multitemplate_st = '<h5 class="category-name text-primary">';
	var multitemplate_et = '</h5>';
	var limit_sugg = 3;
	
	//initialize typehead -> needs to be below source (assignment is in order in js!
	$('#id_search').typeahead(
		{
			highlight: true
			
		},
		{
		  name: 'companies',
		  source: companies,
		  display: 'name',
		  limit: limit_sugg,
		  templates: {
		    header: multitemplate_st + 'Companies' + multitemplate_et
		  }
		},
		{
		  name: 'tags',
		  source: tags,
		  display: 'name',
		  limit: limit_sugg,
		  templates: {
		    header: multitemplate_st + 'Topics' + multitemplate_et
		  }
		},
		{
		  name: 'countries',
		  source: countries,
		  display: 'name',
		  limit: limit_sugg,
		  templates: {
		    header: multitemplate_st + 'Countries' + multitemplate_et
		  }
		},
		{
		  name: 'references',
		  source: references,
		  display: 'name',
		  limit: limit_sugg,
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
				else if (modname == 'tags'){
					var elt = $('#id_f_tags');
					var el_id = '#id_row_f_tags';					
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
		//var elt = $('#id_f_freetext');
		var elt = $('#id_f_summary');
		var el_id = '#id_row_f_summary';
		
		
		elt.tagsinput('add', val_str);	//adds tag
		$(el_id).show();
		//$('#id_row_f_freetext').show();
		//$(this).val(''); 
		$(this).typeahead('val', ''); //typeahead input
		
		
	});
	$('.topic-link').click(function(){
		var tagname = $(this).attr('tagname');
		var tagid = parseInt($(this).attr('tagid'));
		set_tag(tagid, tagname)
		
	});
	
	$("#id_search").keyup(function(event) {
	    if (event.keyCode === 13) { //enter
	    	var e = jQuery.Event("keydown");
	    	e.which = e.keyCode  = 40; // down arrow
	    	$(this).trigger(e);
	    	e.which = e.keyCode  = 9; // tab key
	    	$(this).trigger(e);
	    	//in case there is no suggestion:
	        $(this).blur();
	        $(this).focus();
	    }
	});

});

var drawcharts = false; 

function set_val_from_btn(event) {
	var el_id = '#' + event.target.id;
	var id_val = Number(event.target.name);
	var input_id = '#' + $(event.target).attr('targfield');
	var pressed = event.target.attributes['aria-pressed'].value; // true or false

	var el_val = $(input_id).val();
	var val_list = JSON.parse("[" + el_val + "]"); 

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
 				  'date', 'date_sort', 'reference_sort', 'sudom_sort',
 				  'id'],
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
 	impevList.sort('date_sort', { order: "desc" }); //as to start
}



function set_filterbtns_notused(){
	$.each(btns_dict, function( k, v ) {
		var part_id = '#id-' + k + '-btn-';	//k = sust_domain or sust_tendency
		$.each(v, function(index, val_i){
			var btn_id = part_id + val_i;
			//$(btn_id).addClass("active");
			$(btn_id).click(); //clicks and adds to hidden input
			});
	});	
}

function toggle_visibility(jqid) {
    var e = $(jqid);
    if(e.hasClass('show')){
    	e.removeClass('show');
    	}
       
    else {
       e.addClass('show');
    }
 }

//set tags from topics
function set_tag(id, tagname) {
	var suggestion = {'id': id, 'name': tagname};
	var elt = $('#id_f_tags');
	var el_id = '#id_row_f_tags';
	elt.tagsinput('add', suggestion);	//adds tag	
	$(el_id).show();	
	
}


function toggle_filter_frombtn() {
	
	toggle_filter(fshow = true) ; //show always
	var hi = $('#id_contsearch').outerHeight() + 10; //smaller than navbar id_navbar
	$([document.documentElement, document.body]).animate({
	    scrollTop: $("#div_filterform").offset().top - hi
	}, 'slow');
}

function toggle_filter(fshow = false) {	
	if ($('#filterform').hasClass('show') && fshow == false){
		$('#div_filterform').addClass('nobackground');
		$('#div_filterform .show').removeClass('show'); 
		$('#divFilterHead .showopposite').addClass('show'); 
	}
	else {
		$('#div_filterform').removeClass('nobackground');	
		$('#div_filterform .collapse').addClass('show');
		$('#divFilterHead .showopposite').removeClass('show'); 
	}
}

var ie_details = ''; 
var comp_ratings = ''; 

function setData(response) {
	var tblData = response.table_data;
	var compData = response.comp_details;
	var msg = response.message;
	
	ie_details = JSON.parse(response.ie_details); 
	comp_ratings = JSON.parse(response.comp_ratings); 
	
	$("#id_message").html(msg);
	
	drawcharts = true;
	//when google is loaded
	google.charts.setOnLoadCallback(drawCharts);
	
	$("#company-details-row").html(compData);
	$("#id_ovtable").html(tblData);
	
	set_topheadaer()//new th elements
	prepare_list();

}

function submitFilterForm(ev){
	var target = $(ev.target);
	if (target.hasClass('nosubmit')){
		target.removeClass('nosubmit');
	}
	else {
		var foid = '#' + ev.target.form.id;
		$(foid).submit();
	}	
}

function setFilterIcon(){
	var validate= false;
	var filterCount = 0;
	$('.f_input').each(function(){
	    if($(this).val() != ''){
	    	filterCount ++;
	        validate = true;
	    } 
	       
	});
	if(!validate){
		
		$('#icon_filter_active').hide();
		$('#icon_filter').show();				
	}
	else { 
		$('#icon_filter').hide();
		$( '#icon_filter_active' ).show();	
		var $el = $('#btn_filter_toggle'),
	    	originalColor = $el.css("background");

		$el.attr('style', "background: #ffff99 !important"); //due to mdb
		setTimeout(function(){
			$el.animate({
				backgroundColor: originalColor
			}, 100, function() {
				$el.removeAttr('style');
			  });													
		}, 200);

	}
	$('#filter-count').html(filterCount);
}

function setFilterVisually(filterDict){
	var filterCount = 0;
	$('.f_input').each(function(){
		
		var ele = $(this);
	    if (ele.val() != ''){
	    	filterCount ++;
	    	var val = ele.val();
	    	var parfield =  ele.attr('parfield');
	    	var el_name =  ele.attr('name');
	    	var valList = filterDict[el_name];
	    	if (ele.hasClass('btninput')){
	    		ele.val(valList); //value set from filter is string incl. [
	    		$.each(valList, function(index, value ){
	    			//todo check but should only ids
		    		var targetId =  parfield + value;	    		
		    		$(targetId).attr('aria-pressed', 'true');
		    		$(targetId).addClass('active');
	    		});
	    	} else if (ele.hasClass('f_tagsinput')) {
	    		function addTag(suggestion){
	        		ele.addClass('nosubmit');
	        		ele.tagsinput('add', suggestion);	
	    		}
	    		
	    		var targetId =  parfield + el_name; //eg company
	    		if (el_name == 'summary'){
	    			addTag(val)		    			
	    		} else {
		    		
	    			$.each(valList, function(index, value ){
	    				var suggestion = value; //filterDict[value] ;   		
	    				addTag(suggestion)	    				
			    		});
	    		}
	    		$(targetId).show();		
	    	} else if (ele.hasClass('dateyearpicker')){
	    		
	    		//ele.data("DateTimePicker").date(val);
	    		
	    	}

	    	$('#icon_filter').hide();
			$( '#icon_filter_active' ).show();	
	    	    	
	    }
	});
	$('#filter-count').html(filterCount);
}

function clearFilter() {
	var filterCount = 0;
	$('.f_tagsinput').each(function(){
		
		var ele = $(this);
	    if (ele.val() != ''){
	    	ele.addClass('nosubmit');
	    	ele.tagsinput('removeAll');
	    }
	});
	
	$('.btnselect').attr('aria-pressed', 'false');
	$('.btnselect').removeClass('active');
	$('.row_tags_class').hide();
	
	$('.f_input').each(function(){
		
		var ele = $(this);
	    if (ele.val() != ''){
	    	ele.addClass('nosubmit');
	    	ele.val('');
	    	}
	    });
	$('#id_filterform').submit();
}



//initialize BLOODHOUND
function getBloodhoundOpt(field_url){
	optDict = {
			  datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'), //obj.whitespace('name') -> data needs to be transformed
			  queryTokenizer: Bloodhound.tokenizers.whitespace, 
			  //identify: function(obj) { return obj.id; }, //to get suggestion by ID -> not used and breaks typahead!
			  prefetch: {
				  url: field_url, // url set in html
				  cache: true	 // defaults to true -> for testing	        
			        },
	}
	return optDict
}
var bldhndOptComp = new getBloodhoundOpt(companies_url);
var companies = new Bloodhound(bldhndOptComp);

var optCountries = new getBloodhoundOpt(countries_url);
var countries = new Bloodhound(optCountries);

var optReferences = new getBloodhoundOpt(references_url);
var references = new Bloodhound(optReferences);

var optTopics = new getBloodhoundOpt(tags_url);
var tags = new Bloodhound(optTopics);


