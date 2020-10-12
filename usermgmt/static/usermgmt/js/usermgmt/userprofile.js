/**
 *
 */

// jquery
$(document).ready(function () {
    // pass options to ajaxForm
    $(formId).ajaxForm(formoptions); //id_div_impevform

});
// form ajax options
const messageId = '#id_up_message';
const formId = '#id_userform';

const formoptions = {
    success: function (response) {
        const msg = response.message;
        $(messageId).html(msg);
        errorHandling(formId, response, messageId);
    },
    error: function (response) {
        $(messageId).html('uups');
    }
}
