/**
 *
 */

// jquery

$(document).ready(function () {
    //set automatically 1st of jan
    $(".dateyearpicker").on(
        'dp.update',
        function (e) { // e = event
            set_firstjan(e, this);

        });

    $(window).resize(function () { //window changes-> a lot need to be handled
        var timeout = false, // holder for timeout id
            delay = 400; // delay after event is "complete" to run callback
        // clear the timeout
        clearTimeout(timeout);
        // start timing for event "completion"
        timeout = setTimeout(set_topheadaer, delay);
    });

    set_topheadaer();


});

//set automatically 1st of jan
function set_firstjan(e, element) { // e = event

    var changed = e["change"];
    if (changed == 'YYYY') { // if year changed
        var dt = e.viewDate._d;
        var year_i = dt.getFullYear() // integer
        if (e.viewDate._i) { // last date
            var m_str = e.viewDate._i.substring(0, 6);
        } else {
            var m_str = '01.01.';
        }
        var date_str = m_str + year_i.toString();
        $(element).data("DateTimePicker").clear();
        $(element).data("DateTimePicker").date(date_str);
        $(element).data("DateTimePicker").defaultDate(date_str);
        $(element).data("DateTimePicker").hide()
    }
}


function set_topheadaer() {
    let hNavbar = $('#id_contsearch').outerHeight(); //smaller than navbar id_navbar
    let hFilter = $('#divFilterBar').outerHeight(); //smaller than navbar id_navbar
    let hTotal = hNavbar; //+  hFilter;
    //$('#divFilterBar').css({ top: hNavbar });
    $('.table-etiki th').css({top: hTotal});
    let hAnchor = hNavbar + 5;
    $('.anchor').css({'padding-top': hAnchor});
    $('.anchor').css({'margin-top': -hAnchor });
}