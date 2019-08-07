/**
  
 */

//jquery


$(document).ready(function() {
   
	
	$("#id_year").on('dp.update', function(e){  //e = event
		
		var year_str = $(this).val();
		
		$('#id_date_published').data("DateTimePicker").defaultDate(year_str);

	  });
	
	

});



