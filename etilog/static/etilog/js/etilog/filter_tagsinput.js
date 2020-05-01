$(document).ready(function () {
    //add tagsinput and typeahead on hidden fields
    $('.f_tagsinput').each(function () {
        var ele_name = $(this).attr('name');
        var optDic = allTypeaheadDic[ele_name];
        if (optDic) {
            $(this).tagsinput({
                itemValue: 'id',
                itemText: 'name',
                itemCategory: 'category',
                typeaheadjs: [
                    {
                        highlight: true,
                        autoselect: true,
                    },
                    optDic,
                ],
            });
            }
        else { //free text
            $(this).tagsinput();

        }
            var plcHolder = $(this).attr('placeholder');

            var parentId = $(this).attr('parfield');
            $(parentId).find('.bootstrap-tagsinput input.tt-input').attr('placeholder', plcHolder);


        ;
    });



    $('.f_tagsinput').on('itemRemoved', function (event) {
        if ($(this).tagsinput('items').length == 0) {
            var parentId = $(this).attr('parfield');
            $(parentId).removeClass('show');
        }

    });



});

//set tags from topics
function set_tag(id, tagname) {
    var suggestion = {'id': id, 'name': tagname};
    var ele = $('#id_f_tags');
    setTags(ele, suggestion);

}

function setTags(ele, suggestion) {
    ele.tagsinput('add', suggestion);	//adds tag
    let parentId = ele.attr('parfield');
    $(parentId).addClass('show');
    // todo >, on delete -> delete
    const eleAllTags = $('#id_alltaginput_todo');
    eleAllTags.tagsinput('add', suggestion);	//adds tag

}


function setTagBtn(eleId) {
    const ele = $('#' + eleId);
    if (setFirstSelection(ele) === false) {
        changeWOSelection(ele);
    }
    ;
}