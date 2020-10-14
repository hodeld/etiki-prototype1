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

        if (response.redirect) {
            messageHandling (messageId, response);
            window.location.href = response.redirect;
        }
        else {
            formErrorHandling(formId, response, messageId);
        }


    },
    error: function (response) {
        formErrorHandling(formId, response, messageId); // error get jqXHR as argument
       //messageHandling(messageId, undefined, 'uups', 'error')
    }
}
