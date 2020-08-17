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


    $('._f_tags_search_inp').on('beforeItemAdd', function (event) {
        let suggestion = event.item;
        suggestion.category = 'reference_exc';
        setTags(suggestion, allTags = false);
    });

    $('._f_tags_search_inp').on('beforeItemRemove', function (event) {
        let suggestion = event.item;
        suggestion.category = 'reference_exc';
        removeTags(suggestion);
    });


    $('._f_tags_search_inp').typeahead(
        {
            highlight: true,
            autoselect: true,
        },
        countriesTa,
    );

    $('._f_tags_search_inp').bind('typeahead:select', function (ev, suggestion) {
        //from search directly table
        const val_str = suggestion['name'];
        if (val_str.length > 0) {
            suggestion.category = 'reference_exc';
            setTags(suggestion);
            $(this).typeahead('val', ''); //typeahead input
        }
    });

    $('.div_search_typeahead.free_input .input-group-append').click(function(){
        let ele = $(this);
        setTagBtn(ele);
    });

    $('.div_search_typeahead.not_free_input .input-group-append').click(function(){
        let ele = $(this);
        setTagBtn(ele, false);
    });

});


//for topics??
function setTagBtn(ele, freeInput=true) {
    if (freeInput){
        if (setFirstSelection(ele) === false) {
            changeWOSelection(ele);
        }
    }
    else {
        setFirstSelection(ele)
    }

}

function setFirstSelection(ele) {
    const firstsel = ele.parent().find('.tt-selectable:first');
    if (firstsel.length > 0) {
        firstsel[0].click();
    } else {
        return false;
    }
}

//if changed without suggestion
function changeWOSelection(ele) {
    const val_str = ele.typeahead('val');
    if (val_str){ // can be undefined
        let suggestion = {
            'id': val_str,
            'name': val_str,
            'category': 'summary'
        };
        setTags(suggestion);
        ele.typeahead('val', ''); //typeahead input
    }
    ele.focus();
}


function keyBehaviorSearch(event, ele) {
    if (event.keyCode === 13) { //enter
        if (ele.val()!== '') {
            changeWOSelection(ele);
        }
    }
}

const limit_sugg = 5;

//var compTa = new getTypeaheadOpt('company', companies, limit_sugg);

//var refTa = new getTypeaheadOpt('reference', references, limit_sugg);

let countriesTa = new getTypeaheadOpt('country', countries, limit_sugg);

//var tagsTa = new getTypeaheadOpt('tags', tags, limit_sugg);


var allTypeaheadDic = {
    //'tags': tagsTa,
    //'company': compTa,
    //'reference': refTa,
    'country': countriesTa,
};