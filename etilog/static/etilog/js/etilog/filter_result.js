/**
 *
 */

// jquery
$(document).ready(function () {


    $('#tab1[data-toggle="tab"]').on('shown.bs.tab', function (e) {
        viewType = 'company';
        if (companyGet) {
            getResults();
            companyGet = false;
        }
        drawCharts();
        return false

    });

    $('#tab2[data-toggle="tab"]').on('shown.bs.tab', function (e) {
         viewType = 'table';
        if (tableGet) {
            getResults();
            tableGet = false;
        }
        return false

    });

    $('#tab3').click(function () {
        $('#networkAnyCompany').addClass('show');
        $('#networkCompany').removeClass('show');
    })


});
let companyGet = true;
let tableGet = true;
let detailsGet = true;
let viewType = 'company'; // or table or imp_detail

const resultOptions = {
    beforeSubmit: function (arr, $form, options) {
        $("#id_message").html('calculating results …');

    },
    success: function (response) {
        setResultData(response);
    },
    url: result_url, //needed to be defined due to searchurl

};

let resultOptsBG = {...resultOptions};
resultOptsBG.beforeSubmit = null;

function getResults(){
    resultOptions.data = {result_type: viewType};
    $.ajax(resultOptions); // ajax request without form submit
    return false;
}

function getResultsInBG(){
    //load all other results in background
    //if in table view -> first details than companies
    //in in company view -> first table than details
    if (tableGet) {
        resultOptsBG.data = {result_type: 'table'};
        $.ajax(resultOptsBG); // ajax request without form submit
        tableGet = false;
    }
    if (detailsGet) {
        resultOptsBG.data = {result_type: 'ie_detail'};
        $.ajax(resultOptsBG); // ajax request without form submit
        detailsGet = false;
    }
    if (companyGet) {
        resultOptsBG.data = {result_type: 'company'};
        $.ajax(resultOptsBG); // ajax request without form submit
        companyGet = false;
    }
}