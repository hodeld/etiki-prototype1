$(document).ready(function () {
    //add tagsinput and typeahead on hidden fields
    $('.f_tagsinput').each(function () {
        let ele_name = $(this).attr('name');
        let optDic = allTypeaheadDic[ele_name];
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
        let plcHolder = $(this).attr('placeholder');

        let parentId = $(this).attr('parfield');
        $(parentId).find('.bootstrap-tagsinput input.tt-input').attr('placeholder', plcHolder);


        ;
    });


    $('.f_tagsinput').on('beforeItemRemove', function (event) {
        resultType = 'count';
        const eleId = '#id_alltaginput';
        removeTags(eleId, event);
    });

    $('#id_alltaginput').tagsinput({
        itemValue: 'id',
        itemText: 'name',
        itemCategory: 'category',
    });

    $('#id_alltaginput').on('beforeItemRemove', function(event) {
        resultType = 'data';
        const eleId = tagElementDict[event.item.category] || '#id_f_freetext';
        removeTags(eleId, event);
    });


    $('.topic-link').click(function () {
        let tagname = $(this).attr('tagname');
        let tagid = parseInt($(this).attr('tagid'));
        let tagCategory = $(this).attr('tag-category');
        resultType = 'data';
        let suggestion = {
            'id': tagid,
            'name': tagname,
            'category': tagCategory
        };
        setTags(tagCategory, suggestion)
    });


});

const tagElementDict  = {
    'companies': '#id_f_company',
    'countries': '#id_f_country',
    'references': '#id_f_reference',
    'tags': '#id_f_tags',
}

function setTags(category, suggestion) {
    const eleId = tagElementDict[category] || '#id_f_freetext';
    const ele = $(eleId);
    suggestion.category = category;

    ele.tagsinput('add', suggestion);	//adds tag
    let parentId = ele.attr('parfield');
    $(parentId).addClass('show');
    // todo >, on delete -> delete
    const eleAllTags = $('#id_alltaginput');
    eleAllTags.tagsinput('add', suggestion);	//adds tag
}

function removeTags(eleId, event) {
    let evOpt = {};
    if (event.options ) {
        if (event.options.preventRemove){
            event.cancel = true;
            return false;
        }
        else if (event.options.firstRemove){
            evOpt.preventRemove = true;
        }
    }
    else {
        evOpt.firstRemove = true;
    }
    const ele = $(eleId);
    ele.tagsinput('remove', event.item, evOpt);	//adds tag
}

function setTagBtn(eleId) {
    const ele = $('#' + eleId);
    if (setFirstSelection(ele) === false) {
        changeWOSelection(ele);
    }
    ;
}