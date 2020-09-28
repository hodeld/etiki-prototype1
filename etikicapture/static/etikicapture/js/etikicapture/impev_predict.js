/**
 *
 */

// jquery
$(document).ready(function () {

});

function predictImpEv(response){
    if (!response.prediction){
        return false;
    }
    const tendId = response.tendency_id;
    const eleId = 'sust_tendency' + tendId;
    const ele = $('#'+ eleId);
    ele.prop('checked', true);
}