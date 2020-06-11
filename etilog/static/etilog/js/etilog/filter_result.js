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

function getResultsInBG(viewName='table'){
    if (viewName === 'table') {
        if (tableGet) {
            resultOptsBG.data = {result_type: viewName};
            $.ajax(resultOptsBG); // ajax request without form submit
            tableGet = false;
        }

    }
    if (viewName === 'company') {
        if (companyGet) {
            resultOptsBG.data = {result_type: viewName};
            $.ajax(resultOptsBG); // ajax request without form submit
            companyGet = false;
        }

    }
}