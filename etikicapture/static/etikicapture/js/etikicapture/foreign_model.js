/**
 *
 */

// jquery

$(document).ready(function () {

    $(".add_foreignmodel").click( //to each element with this class
        function () {
            const get_url = $(this).attr("add-url"); // model_name in url
            const fieldId = $(this).attr("field-id");
            //var wname = url.substring(0, 5);
            $.ajax({
                url: get_url, // set the url of the request (= '')
                success: function (response) { // `data` is the return of the
                    //var msg = response.message;
                    const parID = '#id_foreign_body';
                    $(parID).html(response);
                    initTagInput(parID);
                    $('#fModelSave').click(function(){
                        saveFModel()
                    });
                    $('#id_field_id').val(fieldId);
                    $('#div_addforeign').modal('show');
                },
                error: function () {
                    $("#id_impev_msg").html('there was an error');
                }

            });
            //w = window.open(url, wname,"width=600, height=800, scrollbars=yes");
        });


});
function saveFModel(){
    const fMoOpts = {
        //url: get_url, // set the url of the request (= '')
        success: function (response) {
            if (response.is_valid == 'true') {
                const fieldId = $('#id_field_id').val();
                $('#'+fieldId).tagsinput('removeAll');
                $('#'+fieldId).tagsinput('add', response.tag);
                $('#div_addforeign').modal('hide');
            } else {
                const parID = '#id_foreign_body';
                $(parID).html(response.form_html);
                initTagInput(parID);
            }
        }
    };
    $('.foreignModel').ajaxSubmit(fMoOpts);
}



function closeModal(win, newID, newRepr, id) {
    //closes modal if form is valid

    var elem = document.getElementById(id);
    var idj = "#" + id
    if (elem) {
        var elemName = elem.nodeName.toUpperCase();
        if (elemName === 'SELECT') {
            $(idj).append(
                '<option value=' + newID + ' selected >' + newRepr
                + '</option>');

        } else {
            $(idj).val(newRepr);

        }
    }

    win.close();

}
