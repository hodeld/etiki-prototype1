$(document).ready(function () {

    //send element as with event.target it can be fa-icon!
    $('.btnselect').click(function () {
        set_val_from_btn($(this))
    });

    $('.filterClear').click(function () {
        clearFilter()
    });
    $('.filterClearDirect').click(function () {
        clearFilter()
    });

    //directly submit on filterinputs:
    $('.f_input').change(function (ev) {
        submitFilterForm();
    });

    //directly submit on datetimeinput
    $(".dateyearpicker").on('dp.change', function (ev) { // e = event
        submitFilterForm();
    });


});

let submit = true;

function set_val_from_btn(ele) {
    //mirror_btn(ele);
    const idVal = Number(ele.attr('name'));
    const inputId = '#' + ele.attr('targfield');

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
    if (addValue) {
        const len = val_set.size ;
        val_set.add(idVal);
        filterCount += (val_set.size-len);
    } else {
        filterCount--;
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


function clearFilter() {
    filterCount = 0;
    submit = false;
    $('.f_alltagsinput, .f_tags_search_inp').each(function () {
        var ele = $(this);
        if (ele.val() !== '') {
            ele.tagsinput('removeAll');
        }
    });



    $('.btnselect').attr('aria-pressed', 'false');
    $('.btnselect').removeClass('active');
    $('.row_tags_class').hide();
    $('.f_input').each(function () {
        var ele = $(this);
        if (ele.val() != '') {
            ele.val('');
        }
    });
    submit = true;
    submitFilterForm();
}





