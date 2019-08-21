/**
 * 
 */

// jquery

$(document).ready(function() {
	 $(".autocompwidget").each(function(){
		 var list_str = $(this).attr("data_list");
		 var el_list = list_str.split(";");
		 autocomplete($(this)[ 0 ], el_list); //Equivalent to document.getElement...
	 });
	

	$("#add_id_company").click( function() { 
		var url = $(this).attr("add-url"); //model_name in url
		w = window.open(url, "id_company", "width=600, height=800, scrollbars=yes");
		
		//var win = window.open(url, "popupWindow", "width=600, height=800, scrollbars=yes");
		//win.focus();
        //return false;
		

	});
	
	$("#add_id_reference").click( function() { 
		var url = $(this).attr("add-url");
		window.open(url, "id_reference", "width=600, height=800, scrollbars=yes");

	});
	

	

	$("#id_sust_domain").change(function() { // jquery code $# -> gives ide; if radioselect: id_id_sust_domain_0_2
		var url = $("#id_sust_category").attr("data-susts-url"); // get the url of

		var domainId = $(this).val(); // get the selected Domain ID from the
										// HTML input
		// var cachname = $("#dateForm").attr("cachname_tbldict");
		$.ajax({ // initialize an AJAX request
			url : url, // set the url of the request (= '')
			data : {
				'domainId' : domainId
			// add the domainId to the GET parameters
			},
			success: function (data) {   // `data` is the return of the `load_susts` view function
		          $("#id_sust_category").html(data);  // replace the contents of the sust input with the data that came from the server
		        }

		});
	});
	
	$("#id_sust_category").change(function() { // jquery code $# -> gives ide; if radioselect: id_id_sust_domain_0_2
		var url = $("#id_sust_tags").attr("data-tags-url"); // get the url of

		var categoryId = $(this).val(); // get the selected category ID from the
										// HTML input
		$.ajax({ // initialize an AJAX request
			url : url, // set the url of the request (= '')
			data : {
				'categoryId' : categoryId
			// add the categoryId to the GET parameters
			},
			success: function (data) {   // `data` is the return of the `load_susts` view function
		          $("#id_sust_tags").html(data);  // replace the contents of the sust input with the data that came from the server
		        }

		});
	});
	
	
	$("#id_year").on('dp.update', function(e) { // e = event

		var year_str = $(this).val();
		var date_str = '01.01.' + year_str;
		
		$('#id_date_published').data("DateTimePicker").clear();
		$('#id_date_published').data("DateTimePicker").defaultDate(date_str);

	});

});

function closePopup(win, newID, newRepr, id) {
    // for select $(id).append('<option value=' + newID + ' selected >' + newRepr + '</option>')
	//var name = windowname_to_id(win.name);
    var elem = document.getElementById(id);
    var idj = "#" + id
	if (elem) {
        var elemName = elem.nodeName.toUpperCase();
        if (elemName === 'SELECT') {
        	$(idj).append('<option value=' + newID + ' selected >' + newRepr + '</option>');
            
        } 
        else  {
        	$(idj).val( newRepr );
            
            }
	}
        
    win.close();

}

function autocomplete(inp, arr) {
	  /*the autocomplete function takes two arguments,
	  the text field element and an array of possible autocompleted values:*/
	  var currentFocus;
	  /*execute a function when someone writes in the text field:*/
	  inp.addEventListener("input", function(e) {
	      var a, b, i, val = this.value;
	      /*close any already open lists of autocompleted values*/
	      closeAllLists();
	      if (!val) { return false;}
	      currentFocus = -1;
	      /*create a DIV element that will contain the items (values):*/
	      a = document.createElement("DIV");
	      a.setAttribute("id", this.id + "autocomplete-list");
	      a.setAttribute("class", "autocomplete-items");
	      /*append the DIV element as a child of the autocomplete container:*/
	      this.parentNode.appendChild(a);
	      /*for each item in the array...*/
	      for (i = 0; i < arr.length; i++) {
	        /*check if the item starts with the same letters as the text field value:*/
	        if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
	          /*create a DIV element for each matching element:*/
	          b = document.createElement("DIV");
	          /*make the matching letters bold:*/
	          b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
	          b.innerHTML += arr[i].substr(val.length);
	          /*insert a input field that will hold the current array item's value:*/
	          b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
	          /*execute a function when someone clicks on the item value (DIV element):*/
	              b.addEventListener("click", function(e) {
	              /*insert the value for the autocomplete text field:*/
	              inp.value = this.getElementsByTagName("input")[0].value;
	              /*close the list of autocompleted values,
	              (or any other open lists of autocompleted values:*/
	              closeAllLists();
	          });
	          a.appendChild(b);
	        }
	      }
	  });
	  /*execute a function presses a key on the keyboard:*/
	  inp.addEventListener("keydown", function(e) {
	      var x = document.getElementById(this.id + "autocomplete-list");
	      if (x) x = x.getElementsByTagName("div");
	      if (e.keyCode == 40) {
	        /*If the arrow DOWN key is pressed,
	        increase the currentFocus variable:*/
	        currentFocus++;
	        /*and and make the current item more visible:*/
	        addActive(x);
	      } else if (e.keyCode == 38) { //up
	        /*If the arrow UP key is pressed,
	        decrease the currentFocus variable:*/
	        currentFocus--;
	        /*and and make the current item more visible:*/
	        addActive(x);
	      } else if (e.keyCode == 13) {
	        /*If the ENTER key is pressed, prevent the form from being submitted,*/
	        e.preventDefault();
	        if (currentFocus > -1) {
	          /*and simulate a click on the "active" item:*/
	          if (x) x[currentFocus].click();
	        }
	      }
	  });
	  function addActive(x) {
	    /*a function to classify an item as "active":*/
	    if (!x) return false;
	    /*start by removing the "active" class on all items:*/
	    removeActive(x);
	    if (currentFocus >= x.length) currentFocus = 0;
	    if (currentFocus < 0) currentFocus = (x.length - 1);
	    /*add class "autocomplete-active":*/
	    x[currentFocus].classList.add("autocomplete-active");
	  }
	  function removeActive(x) {
	    /*a function to remove the "active" class from all autocomplete items:*/
	    for (var i = 0; i < x.length; i++) {
	      x[i].classList.remove("autocomplete-active");
	    }
	  }
	  function closeAllLists(elmnt) {
	    /*close all autocomplete lists in the document,
	    except the one passed as an argument:*/
	    var x = document.getElementsByClassName("autocomplete-items");
	    for (var i = 0; i < x.length; i++) {
	      if (elmnt != x[i] && elmnt != inp) {
	      x[i].parentNode.removeChild(x[i]);
	    }
	  }
	}
	/*execute a function when someone clicks in the document:*/
	document.addEventListener("click", function (e) {
	    closeAllLists(e.target);
	});
	} 
