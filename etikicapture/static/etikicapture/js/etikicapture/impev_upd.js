/**
 *
 */

// jquery
$(document).ready(function () {

    // form ajax options
    var formoptions = {
        success: function (response) {
            var msg = response.message;
            if (response.is_valid == "false") {
                //$("#id_impev_msg").html(JSON.stringify(msg));
                $("#id_impev_msg").html(msg);
                var error_items = response.err_items;
                error_items.forEach(function (item, index) {
                    var el_id = '#id_' + item;
                    $(el_id).addClass('is-invalid') //django class
                });

                //$("#id_impevform").html(response.form); // to show errors
            } else {
                $("#id_impev_msg").html(msg);
                $('.is-invalid').removeClass('is-invalid') //django class
                window.history.pushState("", "", response.upd_url);
                window.scrollTo(0, 0);
            }
        }

    };
    // pass options to ajaxForm
    $('#id_impevform').ajaxForm(formoptions); //id_div_impevform

    $('.swselect').click(function () {
        setValSwitch($(this))
    });


    $("#id_sust_domain").change(function () {
        load_tags();
    });

    $("#id_sust_tendency").change(function () {
        load_tags();
    });

    $("#id_year").on('dp.update', function (e) { // e = event

        var year_str = $(this).val();
        var date_str = '01.01.' + year_str;

        $('#id_date_published').data("DateTimePicker").clear();
        $('#id_date_published').data("DateTimePicker").defaultDate(date_str);

    });
    hide_img_vid();

});

function next_ie() {
    window.location.href = next_id_url; //as user clicked on a link
}

function new_ie() {
    $('#id_impevform').trigger("reset");
    //$('.autocompwidget').val(''); $('textarea').val('');

    $('#id_article_text').val('');
    $("#id_articleshow").html('');
    $("#id_titleshow").html('');
    $("#id_url_link").html('');
    $("#id_url_link").attr("href", '');
    load_tags()
    window.history.pushState("", "", new_ie_url);
}


function extract_text(ele) {
    var source_url = $("#id_c_source_url").val();
    var get_url = $(ele).attr("url-get"); // get

    $("#id_impev_msg").html('reads text from website …');
    window.scrollTo(0, 0);
    $.ajax({ // initialize an AJAX request
        url: get_url, // set the url of the request (= '')
        data: {
            // both can be null
            'sourceurl': source_url
        },
        success: function (response) { // `data` is the return of the
            var msg = response.message;
            if (response.is_valid == "true") {
                var text_str = response.stext;
                var stitle = response.stitle;
                var sdate = response.sdate;
                var shtml = response.shtml;

                $("#id_date_text").val(sdate);
                $("#id_article_text").html(text_str);
                $("#id_article_title").val(stitle);
                $("#id_article_html").val(shtml);
                $("#id_articleshow").html(shtml);

                hide_img_vid()


                $("#id_url_link").html(source_url);
                $("#id_url_link").attr("href", source_url);
                $("#id_titleshow").html(stitle);

            }
            var parse_res = response.parse_res;
            $("#id_result_parse_html").val(parse_res);
            $("#id_impev_msg").html(msg);

        },
        error: function () {
             $("#id_impev_msg").html('there was an error');
        }

    });

}


function hide_img_vid() {
    $('img').hide();
    var vidtags = ["iframe", "video"];
    vidtags.forEach(function (item, index) { //to hide videos
        $(item).each(function (index) {
            $(this).parent().hide();
        });
    });

}

function setValSwitch($ele) {
    const idVal = Number($ele.attr('name'));
    const eleId = $ele.attr('id');
    const inputId = '#' + $ele.attr('data-target');

    let checked = $ele[0].checked;

    const targetEle = $(inputId);
    if (!(targetEle.hasClass('many-values'))){
        const $parent = $ele.closest('.switches_wrap');
        let sel = '.swselect:not(' + '#' + eleId + ')';
        $parent.find(sel).prop('checked', false);
    }

    setFormValue(inputId, idVal, checked);
}

function setFormValue(inputId, idVal, addValue){
    const ele = $(inputId);
    let el_val = ele.val();
    let newVal = '';
    if (ele.hasClass('many-values')){
        let val_set = new Set();
        if (el_val !== '') {
            val_set = new Set(JSON.parse(el_val));
        }
        if (addValue) {
            val_set.add(idVal);
        } else {
            val_set.delete(idVal);
        }
        const newLi = Array.from(val_set);

        if (newLi.length > 0) {
            newVal = JSON.stringify(newLi);
        }
    }
    else {
        if (addValue) {
            newVal = idVal;
        }
    }

    ele.val(newVal)
        .trigger('change'); //needed for hidden input fields

}