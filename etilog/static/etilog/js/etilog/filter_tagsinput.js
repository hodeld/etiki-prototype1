$(document).ready(function () {

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
};

function setTags(suggestion) {
    const eleId = tagElementDict[suggestion.category];
    const idVal = suggestion.id;

    $('.f_alltagsinput').each(function () {
         $(this).tagsinput('add', suggestion);	//adds tag
    });
    setFilterValue(eleId, idVal, addValue=true);
}

function removeTags(suggestion) {
    const eleId = tagElementDict[suggestion.category] || '#id_f_summary';
    const idVal = suggestion.id;
    setFilterValue(eleId, idVal, addValue=false);
}
