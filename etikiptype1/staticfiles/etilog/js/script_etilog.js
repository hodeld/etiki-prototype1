/**
 * 
 */

function toggle(source) {
	var oform = source.form;
    //checkboxes = document.getElementsByName('selection');
    var checkboxes = oform.elements.selection; //can be only 1 element
    if (typeof checkboxes[0] == 'object'){
	    for(var i in checkboxes)
	        checkboxes[i].checked = source.checked;
    }
    else { 
    	checkboxes.checked = source.checked;
    }
}
function confirmRV(rv) {
	var result = rv.value;
	var results = result.split(",");
	var namestr = results[2];	
	var abbr = results[0];
	if (result == "") {
		alert('kein RV gewählt')
		return false}
	string =  namestr + ' als RV bestätigen?'
	return confirm(string);	
}

function action_several(el_value, table = 'ev') {
	var type = el_value;
	if (type == 1){
		str = 'ausgewählte Termine neuplanen?'
	}
	else if (type == 2){
		str = 'ausgewählte Termine löschen?'
	}
	else {str = 'Randtermine planen?'}
	if (table == 'ev'){
		formname = "table_form";
		eventtype = 'ev_act';			
	}
	else if (table == 'zev'){
		formname = "table2_form";
		eventtype = 'zev_act';			
	}
	else {
		formname = "table2_form";
		eventtype = 'sev_act';		
	}
	if (confirm(str)){
    	var oform = document.getElementById(formname);
    	//var formData = new FormData(oform); //formdata from this form
    	var input = document.createElement("input");
        input.setAttribute("type", "hidden");
        input.setAttribute("name", eventtype);
        input.setAttribute("value", type);
        oform.appendChild(input); //appends hidden input field; send request directly did not get response?!
    	oform.submit();
	}
	else {return false}
	}

function filter_sev(id){	
	var oform = document.getElementById("id_sevfilter");

	var masterev = oform["id_masterevent"];
	//var masterev = document.createElement("input");
	//masterev.setAttribute("type", "hidden");
	//masterev.setAttribute("name", "masterevent");
	//masterev.setAttribute("value", id);halo
	masterev.value = id;
	oform.submit();	
}

function change_gs(source, id_str){	
	if (id_str==""){
		id_str = "nogs"
	}
	var oform = source.form;
	var input = document.createElement("input");
    input.setAttribute("type", "hidden");
    input.setAttribute("name", 'gs_id_input');
    input.setAttribute("value", id_str);
    oform.appendChild(input);
	//var gs_id = document.getElementById("id_gs_id");
	//gs_id.value = Number(id_str);

	oform.submit();	
}

function export_evs(form, value){	
	var oform = form;
	var dateform = document.getElementById("id_dateform");
	var dmdateform = document.getElementById("id_dmdateform");
	var exp_type  = document.getElementById("id_exporttype");
	

	if (value=="2" || value=="3" || value=="7"){ //export_juch; Einladung PDF
		dateform.style.display = "";

	}
	
	else if (value=="1" || value=="4" || value=="5"){ //calendar or all events or ctrlist
		dateform.style.display = "none";
		//el_date.type= "hidden";
		//el_btn.type = "hidden";
		if(confirm('Termine exportieren?')){
			oform.submit()
			exp_type.selectedIndex = "0"; 
			}
		else {return false}
		}
	else if (value=="6" ){ //DM events
		dmdateform.style.display = "";
			}
	else{
		
		dateform.style.display = "none";
		dmdateform.style.display = "none";
		exp_type.selectedIndex = "0"; 
		}
	}

function export_excel(form){
	var dateform = form;
	var oform = document.getElementById("id_exportform");
	var el_date = document.getElementById("id_date_export");
	var exp_type  = document.getElementById("id_exporttype");
	var expvalue = exp_type.value;
	if (expvalue == 2){
		conf_str = 'Termine für Juch exportieren?'
	}
	else {conf_str = 'Termine als Einladung exportieren?'
		}
	var dateval = el_date.value;
	if(confirm(conf_str)){
		dateform.style.display = "none";
		var input = document.createElement("input");
	    input.setAttribute("type", "hidden");
	    input.setAttribute("name", 'date_id');
	    input.setAttribute("value", dateval);
	    oform.appendChild(input);
		oform.submit()
		}
	else {
		dateform.style.display = "none";
		return false}
	exp_type.selectedIndex = "0"; 	
}

function export_dmevents(form){
	var dateform = form;
	var oform = document.getElementById("id_exportform");
	var el_date = document.getElementById("id_date_dm");
	var exp_type  = document.getElementById("id_exporttype");
	var expvalue = exp_type.value;
	conf_str = 'alle DM-Termine bis Datum exportieren?'	
	var dateval = el_date.value;
	if(confirm(conf_str)){
		dateform.style.display = "none";
		var input = document.createElement("input");
	    input.setAttribute("type", "hidden");
	    input.setAttribute("name", 'dmdate_id');
	    input.setAttribute("value", dateval);
	    oform.appendChild(input);
		oform.submit()
		}
	else {
		dateform.style.display = "none";
		return false}
	exp_type.selectedIndex = "0"; 	
}
