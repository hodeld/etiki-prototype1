$(document).ready(function () {
    //add tagsinput and typeahead on hidden fields
    $('.f_tagsinput_notused').each(function () {
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
        const suggestion = event.item;
        removeTags(suggestion);
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
        setTags(suggestion);
    });


});

const tagElementDict  = {
    'company': '#id_f_company',
    'country': '#id_f_country',
    'reference': '#id_f_reference',
    'tags': '#id_f_tags',
    'summary': '#id_f_summary',
};

function setTags(suggestion) {
    const eleId = tagElementDict[suggestion.category];
    const idVal = suggestion.id;

    const eleAllTags = $('#id_alltaginput');
    eleAllTags.tagsinput('add', suggestion);	//adds tag
    setFilterValue(eleId, idVal, addValue=true);
}

function removeTags(suggestion) {
    const eleId = tagElementDict[suggestion.category] || '#id_f_freetext';
    const idVal = suggestion.id;
    setFilterValue(eleId, idVal, addValue=false);
}
