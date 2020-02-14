

$(document).ready(function() {

	
	$('.trshowdetails').click(function() {
		toggle_filter()
	});
	
	
});

function numOfVisibleCols(tableid) {
	
	
	var colcnt = $(tableid).find('th').filter(function() { //find as not directly children
	  return $(this).css('display') !== 'none';
	}).length;
	
	return colcnt
}

function show_details(ele, ie_id, event) {
	if (toggle_details(event) == false){
		return;
	} 
	var tableid = '#impev-list';
	var parele = $(ele).parent(); //original row
	var rowid =   ie_id + '_row';
	var detail_id = rowid + '_detail';
	$(parele).addClass('parentrow' )

	var colcnt = numOfVisibleCols(tableid) 
	var rowstr1 = 'tr scope="row" class="detailrow darkbg" id="%%detailid" ';
	var rowstr3 ='<td colspan = "%%colcnt" > %%htmlstr </td> ';	
	var rowstr = '<' + rowstr1 + '>' +  rowstr3 + '</tr>';	
	var html_str = ie_details[ie_id][0];
	rowstr = rowstr.replace("%%htmlstr", html_str);
	rowstr = rowstr.replace("%%colcnt", colcnt);
	rowstr = rowstr.replace("%%detailid", detail_id);
	

	
	$(parele).hide();
	$(parele).after(rowstr);
	$('#'+ detail_id).click(function(event){
		toggle_details(event)		
	});


	
	
}

function toggle_details(event) {
	var target = $( event.target );
	if ( target.is( "button" ) || target.is( "a" ) ) {
		return false;
	}
	else {
	$('.detailrow').hide(); //oder open will be hidden
	$('.parentrow').show(); //oder open will be hidden
	toggle_article(event);
	}
	
}

function full_article(ele, ie_id){
	var parele = $(ele).parent('.showbtn'); //parent div of button
	var detrow = $(ele).parents('.detailrow'); //several levels up
	var detcell = $(ele).parents('td'); //several levels up
	var colcnt = $(detcell).attr('colspan');
	
	var rowstr1 = 'tr scope="row" class="headerrow fullartrow"  ';
	var rowstr2 ='<td class="sticky-top darkbg headertd" colspan = "%%colcnt" > %%htmlstr </td> ';	

	var rowstr = '<' + rowstr1 + '>' +  rowstr2 + '</tr>';
	var html_str = ie_details[ie_id][1]; //header row
	rowstr = rowstr.replace("%%htmlstr", html_str);
	rowstr = rowstr.replace("%%colcnt", colcnt);
	$headerrow= $(rowstr);
	
	var rowstr1 = 'tr scope="row" class="articlerow fullartrow darkbg"  ';
	var rowstr2 ='<td class="articletd" colspan = "%%colcnt" > %%htmlstr </td> ';	
	var rowstr = '<' + rowstr1 + '>' +  rowstr2 + '</tr>';
	var html_str = ie_details[ie_id][2]; //article row
	rowstr = rowstr.replace("%%htmlstr", html_str);
	rowstr = rowstr.replace("%%colcnt", colcnt);
	$artrow = $(rowstr);
	
	$(parele).hide();
	$(detrow).after($headerrow);
	
	$headerrow.after($artrow);
	hide_img_vid();	
	let hi = $('#id_contsearch').outerHeight() - 4; //smaller than navbar id_navbar
	$('.headertd').css({ top: hi }); 
	
	$headerrow.click(function(event){
		toggle_article(event)		
	});
}
function toggle_article(event) {
	$('.fullartrow').hide(); //oder open will be hidden	
	$('.showbtn').show(); //oder open will be hidden	
}


function hide_img_vid(){
	var articleid = '#id_articleshow ' ;
	$(articleid + 'img').hide();
    var vidtags = [articleid + "iframe", articleid + "video"];
    vidtags.forEach(function (item, index) { //to hide videos
    	$( item ).each(function( index ) { 
        	  $( this ).parent().hide();
        });
    });
	
}