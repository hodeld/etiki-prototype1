$(document).ready(function () {


});

var drawcharts = false;

var ie_details = '';
var comp_ratings = '';
var resultMessage = '';

var resultType = 'count';

function setData(response) {
    var responseType = response.result_type;
    $('#filterCountText').html(response.msg_count);
    if (responseType === 'count') {
        $("#id_message").html(resultMessage);
        return
    }
    var tblData = response.table_data;
    var compData = response.comp_details;
    var msg = response.message;

    ie_details = JSON.parse(response.ie_details);
    comp_ratings = JSON.parse(response.comp_ratings);
    resultMessage = msg;
    $("#id_message").html(msg);

    drawcharts = true;
    //when google is loaded
    google.charts.setOnLoadCallback(drawCharts);

    $("#company-details-row").html(compData);
    $("#id_ovtable").html(tblData);

    set_topheadaer();//new th elements
    prepare_list();

}

//form ajax options
var formOptions = {

    beforeSubmit: function (arr, $form, options) {
        $("#id_message").html('calculating results …');
        setFilterIcon();
        if (landing == true) { //means was pressed now
            startanimation(); // only first time when table is hidden
        }
        var form = $form //$('#id_filterform');
        var acturl = form.serialize(); //

        var searchurl = list_url + 'search?' + acturl; //list_url: etilog:home
        window.history.pushState("", "", searchurl); //TODO direct url search


    },
    success: function (response) {
        setData(response)
        resultType = 'count';

    },
    url: list_url, //needed to be defined due to searchurl


};


function submitFilterForm(ev) {
    var target = $(ev.target);
    if (target.hasClass('nosubmit')) {
        target.removeClass('nosubmit');
    } else {

        var foid = '#' + ev.target.form.id;
        submitFromID(foid);
    }
}

function submitFromID(foid) {
    //manipulate extra data
    formOptions.data = {result_type: resultType}
    $(foid).ajaxSubmit(formOptions)

}
