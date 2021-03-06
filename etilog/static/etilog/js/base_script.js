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

function hide_img_vid(idStr='id_articleshow') {
    const articleid = '#' + idStr + ' ';
    $(articleid + 'img').hide();
    var vidtags = [articleid + "iframe", articleid + "video"];
    vidtags.forEach(function (item, index) { //to hide videos
        $(item).each(function (index) {
            $(this).parent().hide();
        });
    });
    $(articleid + 'svg').hide();
}

function messageHandling (msgId, response = null, msg='',
                          msgcls = null,
                          msg2Id=undefined){  //mainly error
    if (response) {
        msg = response.message;
        if (response.message_tag) {
            msgcls = response.message_tag;
        }
    }
    if (msgcls) {
        $(msgId).addClass(msgcls);
    } else {
        $(msgId).removeClass('error');
    }
    $(msgId).html(msg);
    if (msg2Id){
        let msg2 = null;
        if (response) {
            msg2 = response.message2;
        }
        if (msg2) {
            $(msg2Id).html(msg2);
        } else {
            $(msg2Id).html('');
        }
    }
}


function formErrorHandling (parDivId, response, msgId=null){  //mainly error
    if (response.responseJSON){ // if ajax error -> data object in response.responseJSON
        response = response.responseJSON;
    }
    if (msgId){
        messageHandling(msgId, response);
    }
    const divErrorId = '#id_div_errors';
    if ($(divErrorId)) {
        if (response.message_error) {
            $(divErrorId).html(response.message_error);
        } else {
            $(divErrorId).html('');
        }
    }

    $(parDivId).find('.invalid-feedback').remove();
    const error_items = response.err_items;
    const html_base_str = '<span class="invalid-feedback"><strong>%%error</strong></span>';
    for  (let key in error_items) {
        let err = error_items[key];
        let html_str = html_base_str.replace("%%error", err);
        let el_id = '#id_' + key;
        let $ele = $(el_id)
        let parId = $ele.attr('parent-id');
        if (typeof parId !== typeof undefined && parId !== false) {
            $ele = $('#' + parId)
        }
        $ele.after(html_str);
        //$ele.addClass('has-danger');
        //$ele.addClass('is-invalid') //django class
    }
}
