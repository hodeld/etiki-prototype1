/**
 *
 */

// jquery
$(document).ready(function () {
    $("#id_source_url").keydown(function(event){
        const ele = $(this);
        changeGetURL(event, ele);
    });

    // form ajax options
    var formoptions = {
        success: function (response) {
            var msg = response.message;
            if (response.is_valid == "false") {
                formErrorHandling(formId, response, messageId);
            } else {
                $("#id_impev_msg").html(msg);
                formErrorHandling(formId, response, messageId); //to remove spans
                if (userIsIntern){
                    window.history.pushState("", "", response.upd_url);
                }
                else {
                    clearImpForm();
                }
                window.scrollTo(0, 0);
            }
        },
        error: function (response) {
            const msgtxt = 'uups';
            messageHandling(messageId, undefined, msgtxt, 'error');
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
const messageId = '#id_impev_msg';
const formId = '#id_impevform';
userIsIntern = false; // todo

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

function changeGetURL(event, ele) {
    let code = event.keyCode || event.which;
    if (code == 9 || code == 13) {
        event.preventDefault();
        if (ele.val() !== '' && ele.val() !== sourceUrl) {
            extract_text();
        }
    }
}

let sourceUrl = '';

function extract_text() {
    sourceUrl = $("#id_source_url").val();
    const msgtxt = 'reads text from website …'
    messageHandling(messageId, undefined, msgtxt );
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

                fullArticle(html_article);
                predictImpEv(response);


            }
            var parse_res = response.parse_res;
            $("#id_result_parse_html").val(parse_res);
            $(messageId).html(msg);
            $('#div_main_fields').fadeIn("slow");

        },
        error: function () {
            const msgtxt = 'There was an error reading the article. You can save the impact event anyways.';
            messageHandling(messageId, undefined, msgtxt, 'error');
            $('#div_main_fields').fadeIn("slow");
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

function fullArticle(html_str){
    $('#fullArticleContent').html(html_str);
    hide_img_vid();
    $('#modalFullArticle').modal('toggle');
}

function clearImpForm(){
    $('#div_main_fields').fadeOut();
    $('#id_impevform').find("input[type=text], textarea, input[type=url]").val("");
    $('.c_tags_search_inp').each(function () {
        $(this).tagsinput('removeAll');
    });
    $('.c_tags_select').each(function () {
        $(this).tagsinput('removeAll');
    });
    //does not get removed with removeAll
    $('.bootstrap-tagsinput-max').removeClass('bootstrap-tagsinput-max');
    $('.swselect').prop('checked', false);
    load_tags();

}
