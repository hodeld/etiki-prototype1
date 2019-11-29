

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
	$('.detailrow').hide(); //oder open will be hidden
	var tableid = '#impev-list';
	var parele = $(ele).parent(); //original row
	var rowid =   ie_id + '_row';
	var detail_id = rowid + '_detail';
	$(parele).attr('id', rowid )
	

	
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
		hide_details(this,  rowid )		
	});
	
}

function hide_details(ele, pare_id) {
	$(ele).hide();
	$('#'+ pare_id).show();
	
}