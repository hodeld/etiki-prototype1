/**
 *
 */

// jquery

$(document).ready(function () {

    fModelClick();
    
});

const fMoOpts = {
        //url: get_url, // set the url of the request (= '')
        success: function (response) {
            if (response.is_valid == 'true') {
                const fieldId = $('#id_field_id').val();
                $('#'+fieldId).tagsinput('removeAll');
                $('#'+fieldId).tagsinput('add', response.tag);
                // add new items to typeahead
                if (fieldId.includes("company")) {
                    compTa.source.clearPrefetchCache();
                    compTa.source.initialize(true);
                }
                else {
                    refTa.source.clearPrefetchCache();
                    refTa.source.initialize(true);
                }
                $('#div_addforeign').modal('hide');
            } else {
                formErrorHandling ('#id_foreign_body', response, '#id_fmodel_msg');
            }
        }
    };



function fModelClick (){
    $(".add_fm").click( //to each element with this class
        function () {
            const get_url = $(this).attr("add-url"); // model_name in url
            const fieldId = $(this).attr("field-id");
            const fieldName = $(this).attr("field-name");
            //var wname = url.substring(0, 5);
            $.ajax({
                url: get_url, // set the url of the request (= '')
                success: function (response) { // `data` is the return of the
                    //var msg = response.message;
                    const parID = '#id_foreign_body';
                    $(parID).html(response);
                    $('#modalTitle').html(fieldName);
                    initTagInput(parID);
                    $('.fModelSubmit').click(function(){
                        $('#id_submit_fm').click(); // so html5 validation works
                    });
                    $('#id_field_id').val(fieldId);
                    $('.foreignModel').ajaxForm(fMoOpts);


                    //add event on switch elements
                    $('.swselect').click(function () {
                        setValSwitch($(this))
                    });

                    $('#div_addforeign').modal('show');
                    //fModelClick();
                },
                error: function () {
                    messageHandling(messageId, undefined, 'there was an error', 'error', msg2Id);
                }

            });
            //w = window.open(url, wname,"width=600, height=800, scrollbars=yes");
        });
}