$(document).ready(function () {
    $('.etiki-form').ajaxForm(etikiFormOptions)

});

//form ajax options
const etikiFormOptions = {
    beforeSubmit: function (arr, $form, options) {
        $form.clearForm();
    },
    success: function (response, statustext, xhr, $form) {
        $form.find('#form-message').html(response.msg);
    },
};

