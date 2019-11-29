

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
	
	var tableid = '#impev-list'
	var parele = $(ele).parent();
	var colcnt = numOfVisibleCols(tableid) //6; //TODO
	var rowstr = '<tr scope="row" class="detailrow"><td colspan = "%%colcnt" > %%htmlstr </td> ';	
	rowstr = rowstr.replace("%%htmlstr",ie_details[ie_id]);
	rowstr = rowstr.replace("%%colcnt",colcnt);
	
	$(parele).after(rowstr);
}

