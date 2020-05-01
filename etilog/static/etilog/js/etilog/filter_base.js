$(document).ready(function () {
    //button select for categories
    //$('.btnselect').on('click', mirror_btn);

    //send element as with event.target it can be fa-icon!
    $('.btnselect').click(function () {
        set_val_from_btn($(this))
    });

    $('.filterClear').click(function () {
        clearFilter()
    });
    $('.filterClearDirect').click(function () {
        clearFilter('table')
    });



    $('#applyFilter').click(function () {
        resultType = 'table';
        submitFromID('#id_filterform');
    });

    //directly submit on filterinputs:
    $('.f_input').change(function (ev) {
        submitFilterForm(ev)
    });

    //directly submit on datetimeinput
    $(".dateyearpicker").on('dp.change', function (ev) { // e = event
        submitFilterForm(ev)
    });


    //initialize typehead -> needs to be below source (assignment is in order in js!
    $('#id_search').typeahead(
        ...allTaHList //elements of list
    );

    $('#id_search').bind('typeahead:select', function (ev, suggestion) {

        //from search directly table
        resultType = 'table';

        var val_str = suggestion['name'];
        var val_id = suggestion['id'];


        if (val_str.length > 0) {
            var modname = ev.handleObj.handler.arguments[2];
            if (modname == 'companies') {
                var elt = $('#id_f_company');
            } else if (modname == 'countries') {
                var elt = $('#id_f_country');
            } else if (modname == 'references') {
                var elt = $('#id_f_reference');
            } else if (modname == 'tags') {
                var elt = $('#id_f_tags');
            } else {
                var elt = $('#id_f_freetext');

            }
            suggestion.category = modname;

            setTags(elt, suggestion);
            $(this).typeahead('val', ''); //typeahead input
        }


    });


    $('.topic-link').click(function () {
        var tagname = $(this).attr('tagname');
        var tagid = parseInt($(this).attr('tagid'));
        resultType = 'table';
        set_tag(tagid, tagname)

    });

    $("#id_search").keyup(function (event) {
        var ele = $(this);
        keyBehaviorSearch(event, ele);
    });

});



function mirror_btn(ele) {
    var twin_id = '#' + ele.attr('twin-id');
    var twin_ele = $(twin_id);
    var pressed = ele.attr('aria-pressed'); // jquery: true or fals

    if (pressed == "false") { //means was not pressed
        twin_ele.attr('aria-pressed', 'true');
        twin_ele.addClass('active');
    } else {
        twin_ele.attr('aria-pressed', 'false');
        twin_ele.removeClass('active');
    }
}


function set_val_from_btn(ele) {
    mirror_btn(ele);
    var el_id = ele.attr('id');
    var id_val = Number(ele.attr('name'));
    var input_id = '#' + ele.attr('targfield');
    var pressed = ele.attr('aria-pressed'); // true or false

    var el_val = $(input_id).val();
    try {
        var val_set = new Set(JSON.parse("[" + el_val + "]"));
    } catch (err) {
        console.log(err.message);
    }


    if (pressed == "false") { //means was pressed now
        val_set.add(id_val);
    } else {
        val_set.delete(id_val);
    }
    new_li = Array.from(val_set);
    if (ele.hasClass('gettable')) {
        resultType = 'table';
    }

    $(input_id).val(new_li)
        .trigger('change'); //needed for hidden input fields
}


function set_filterbtns_notused() {
    $.each(btns_dict, function (k, v) {
        var part_id = '#id-' + k + '-btn-';	//k = sust_domain or sust_tendency
        $.each(v, function (index, val_i) {
            var btn_id = part_id + val_i;
            //$(btn_id).addClass("active");
            $(btn_id).click(); //clicks and adds to hidden input
        });
    });
}

function toggle_visibility(jqid) {
    var e = $(jqid);
    if (e.hasClass('show')) {
        e.removeClass('show');
    } else {
        e.addClass('show');
    }
}






function clearFilter(locResultType = 'count') {
    var filterCount = 0;
    $('.f_tagsinput').each(function () {

        var ele = $(this);
        if (ele.val() != '') {
            ele.addClass('nosubmit');
            ele.tagsinput('removeAll');
        }
    });

    $('.btnselect').attr('aria-pressed', 'false');
    $('.btnselect').removeClass('active');
    $('.row_tags_class').hide();

    $('.f_input').each(function () {

        var ele = $(this);
        if (ele.val() != '') {
            ele.addClass('nosubmit');
            ele.val('');
        }
    });
    resultType = locResultType;

    submitFromID('#id_filterform');

}





