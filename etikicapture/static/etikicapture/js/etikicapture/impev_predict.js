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
    const catId = response.category_id;
    const t_eleId = 'sust_tendency' + tendId;
    const t_ele = $('#'+ t_eleId);
    //reset switches
    $('.swselect').prop('checked', false);

    t_ele.prop('checked', true);
    const cat_eleId = 'sust_domain_sw' + catId;
    const catele = $('#'+ cat_eleId);
    catele.prop('checked', true);
}