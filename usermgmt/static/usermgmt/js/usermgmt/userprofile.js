/**
 *
 */

// jquery
$(document).ready(function () {
    // pass options to ajaxForm
    $('#id_userform').ajaxForm(formoptions); //id_div_impevform

});
// form ajax options
const formoptions = {
    success: function (response) {
        const msg = response.message;
        $("#id_up_message").html(msg);
    },
    error: function (response) {
        $("#id_up_message").html('uups');
    }
}
