/**
 *
 */

// jquery
$(document).ready(function () {
    $("#id_source_url").blur(function(event){
        const ele = $(this);
        blurGetURL(event, ele);
    });

    // form ajax options
    var formoptions = {
        success: function (response) {
            var msg = response.message;
            if (response.is_valid == "false") {
                errorHandling('#id_impevform', response, '#id_impev_msg');

                //$("#id_impevform").html(response.form); // to show errors
            } else {
                $("#id_impev_msg").html(msg);
                errorHandling('#id_impevform', response, '#id_impev_msg'); //to remove spans
                window.history.pushState("", "", response.upd_url);
                window.scrollTo(0, 0);
            }
        },
        error: function (response) {
            $("#id_impev_msg").html('uups');
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
    load_tags();
    window.history.pushState("", "", new_ie_url);
}

function blurGetURL(event, ele) {
    if (ele.val() !== '' && ele.val() !== sourceUrl) {
        extract_text();
        event.preventDefault();
    }

}

let sourceUrl = '';

function extract_text() {
    sourceUrl = $("#id_source_url").val();

    $("#id_impev_msg").html('reads text from website …');
    window.scrollTo(0, 0);
    $.ajax({ // initialize an AJAX request
        url: extractTextUrl, // set the url of the request (= '')
        data: {
            // both can be null
            'sourceurl': sourceUrl
        },
        success: function (response) { // `data` is the return of the
            var msg = response.message;
            if (response.is_valid == "true") {
                var text_str = response.stext;
                var stitle = response.stitle;
                var sdate = response.sdate;
                const shtml = response.shtml;
                const html_article = response.html_article;

                $("#id_date_text").val(sdate);
                $("#id_article_text").html(text_str);
                $("#id_article_title").val(stitle);
                $("#id_article_html").val(shtml);

                //$("#id_url_link").html(sourceUrl);
                //$("#id_url_link").attr("href", sourceUrl);
                //$("#id_titleshow").html(stitle);
                //$("#id_articleshow").html(shtml);
                fullArticle(html_article);

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

function errorHandling (parDivId, response, msgId=''){
    $(msgId).html(response.error_msg);
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

function fullArticle(html_str){
    $('#fullArticleContent').html(html_str);
    hide_img_vid();
    $('#modalFullArticle').modal('toggle');
}