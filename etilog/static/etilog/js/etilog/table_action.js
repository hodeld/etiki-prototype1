

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

function show_details(ele, ie_id) {
	toggle_details(event);
	var tableid = '#impev-list';
	var parele = $(ele).parent(); //original row
	var rowid =   ie_id + '_row';
	var detail_id = rowid + '_detail';
	$(parele).addClass('parentrow' )

	var colcnt = numOfVisibleCols(tableid) //6; //TODO
	var rowstr1 = 'tr scope="row" class="detailrow" id="%%detailid" ';
	var rowstr3 ='<td colspan = "%%colcnt" > %%htmlstr </td> ';	
	var rowstr = '<' + rowstr1 + '>' +  rowstr3;	
	rowstr = rowstr.replace("%%htmlstr", ie_details[ie_id]);
	rowstr = rowstr.replace("%%colcnt", colcnt);
	rowstr = rowstr.replace("%%detailid", detail_id);
	
	$(parele).hide();
	$(parele).after(rowstr);
	$('#'+ detail_id).click(function(){
		toggle_details(event)		
	});
	
}

function toggle_details(event) {
	var target = $( event.target );
	if ( target.is( "button" ) ) {
		return;
	}
	else {
	$('.detailrow').hide(); //oder open will be hidden
	$('.parentrow').show(); //oder open will be hidden
	}
	
}

function full_article(div_id, ele_id){
	$(div_id).hide();
	$(ele_id).show();
	hide_img_vid();	
}

function hide_full_article(self_id, ele_id){

	$('#' + self_id).hide();
	$(ele_id).show();
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