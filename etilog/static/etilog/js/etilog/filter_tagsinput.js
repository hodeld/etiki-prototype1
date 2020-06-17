$(document).ready(function () {
        //used for reference_exclude
        $('.f_tags_search_inp').each(function () {
        let ele_name = $(this).attr('name');
        let optDic = allTypeaheadDic[ele_name];
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
        let plcHolder = $(this).attr('placeholder');
        let parentId = $(this).attr('parfield');
        $(parentId).find('.bootstrap-tagsinput input.tt-input').attr('placeholder', plcHolder);
    });


    $('.f_tags_search_inp').on('beforeItemAdd', function(event) {
        let suggestion = event.item;
        suggestion.category = 'reference_exc';
        setTags(suggestion, allTags=false);
    });

    $('.f_tags_search_inp').on('beforeItemRemove', function(event) {
        let suggestion = event.item;
        suggestion.category = 'reference_exc';
        removeTags(suggestion);
    });

    $('.f_alltagsinput').tagsinput({
        itemValue: 'id',
        itemText: 'name',
        itemCategory: 'category',
    });

    $('.f_alltagsinput').on('beforeItemRemove', function(event) {
        const suggestion = event.item;
        removeTags(suggestion);
    });


    $('.topic-link').click(function () {
        let tagname = $(this).attr('tagname');
        let tagid = parseInt($(this).attr('tagid'));
        let tagCategory = $(this).attr('tag-category');

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
    'reference_exc': '#id_f_reference_exc'
};

function setTags(suggestion, allTags=true) {
    const eleId = tagElementDict[suggestion.category];
    const idVal = suggestion.id;
    if (allTags) {
        $('.f_alltagsinput').each(function () {
            $(this).tagsinput('add', suggestion);	//adds tag
        });
    }
    setFilterValue(eleId, idVal, addValue=true);
}

function removeTags(suggestion) {
    const eleId = tagElementDict[suggestion.category] || '#id_f_summary';
    const idVal = suggestion.id;
    setFilterValue(eleId, idVal, addValue=false);
}
