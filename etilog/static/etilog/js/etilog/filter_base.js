$(document).ready(function () {
    //button select for categories
    //$('.btnselect').on('click', mirror_btn);

    //send element as with event.target it can be fa-icon!
    $('.btnselect').click(function () {
        set_val_from_btn($(this))
    });

    $('.filterClear').click(function () {
        clearFilter('count')
    });
    $('.filterClearDirect').click(function () {
        clearFilter('data')
    });



    $('#applyFilter').click(function () {
        resultType = 'data';

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
        resultType = 'data';

        const val_str = suggestion['name'];

        if (val_str.length > 0) {
            const category = ev.handleObj.handler.arguments[2];
            suggestion.category = category;
            setTags(suggestion);
            $(this).typeahead('val', ''); //typeahead input
        }

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
    const idVal = Number(ele.attr('name'));
    const inputId = '#' + ele.attr('targfield');
    if (ele.hasClass('gettable')) {
        resultType = 'data';
    }
    const pressed = ele.attr('aria-pressed'); // true or false

    let addValue = false;
    if (pressed == "false") { //means was pressed now
        addValue = true;
    }
    setFilterValue(inputId, idVal, addValue);
}

function setFilterValue(inputId, idVal, addValue) {

    let el_val = $(inputId).val();
    let val_set = new Set();
    if (el_val !== ''){
        val_set = new Set(JSON.parse(el_val));
    }
    if (addValue) { //means was pressed now
        val_set.add(idVal);
    } else {
        val_set.delete(idVal);
    }
    const newLi = Array.from(val_set);
    let newVal = '';
    if (newLi.length > 0) {
        newVal = JSON.stringify(newLi);
    }

    $(inputId).val(newVal)
        .trigger('change'); //needed for hidden input fields
}


function clearFilter(locResultType = 'count') {
    var filterCount = 0;
    $('.f_tagsinput').each(function () {

        var ele = $(this);
        if (ele.val() !== '') {
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





