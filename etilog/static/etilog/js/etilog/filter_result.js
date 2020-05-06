/**
 *
 */

// jquery
$(document).ready(function () {


    $('#tab1[data-toggle="tab"]').on('shown.bs.tab', function (e) {
        viewType = 'company';
        if (companyGet) {
            getResults();
            drawCharts();
            companyGet = false;
        }
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

function getResults(){
    resultOptions.data = {result_type: viewType};
    $.ajax(resultOptions); // ajax request without form submit
    return false;
}
