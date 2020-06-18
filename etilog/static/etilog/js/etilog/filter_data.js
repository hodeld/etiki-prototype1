$(document).ready(function () {


});

let drawcharts = false;

let comp_ratings = '';

function setData(response) {
    if (response.message) { //other messages if new calculated
        setMessages(response);
    }
    getResults();
}

function setResultData(response){
    let responseType = response.result_type;

    if (responseType === 'table') {
        tableGet = false;
        let tblData = response.table_data;
        //ie_details = JSON.parse(response.ie_details);
        $("#id_ovtable").html(tblData);

        set_topheadaer();//new th elements
        prepare_list();
        getResultsInBG();
        return
    }

    if (responseType === 'company') {
        companyGet = false;
        let compData = response.comp_details;
        comp_ratings = JSON.parse(response.comp_ratings);
        drawcharts = true;
        //when google is loaded
        google.charts.setOnLoadCallback(drawCharts);
        $("#company-details-row").html(compData);
        getResultsInBG();
        return
    }
     if (responseType === 'ie_detail') {
         ie_details =  response.ie_details;
     }




}
function setMessages(response){
    // cached or new messages
    $(".filterMessage").html(response.message);
    $(".ie_count").html(response.ie_count);
    $(".company_count").html(response.company_count);

    }


//form ajax options
const formOptions = {

    beforeSubmit: function (arr, $form, options) {
        $("#id_message").html('calculating results …');
        setFilterIcon();
        if (landing == true) { //means was pressed now
            startanimation(); // only first time when table is hidden
        }
        var form = $form;//$('#id_filterform');
        var acturl = form.serialize(); //

        var searchurl = list_url + 'search?' + acturl; //list_url: etilog:home
        window.history.pushState("", "", searchurl);


    },
    success: function (response) {
        companyGet = tableGet = detailsGet = true;
        setData(response);

    },
    url: filter_url, //needed to be defined due to searchurl


};
function submitFilterForm() {
    if (submit) {
        const fId = '#id_filterform';
        //from filter -> first count only
        formOptions.data = {result_type: 'count'};
        $(fId).ajaxSubmit(formOptions);
    }
}

