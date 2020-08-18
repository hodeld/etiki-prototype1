$(document).ready(function () {

        //used for fields in capture
    $('.c_tags_search_inp').each(function () {
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

    $('.c_tags_select').each(function () {
        let ele_name = $(this).attr('name');
        $(this).tagsinput({
            itemValue: 'id',
            itemText: 'name',
            itemCategory: 'category',
            selectTag: true,
        });
        let plcHolder = $(this).attr('placeholder');
        let parentId = $(this).attr('parfield');
        $(parentId).find('.bootstrap-tagsinput input.tt-input').attr('placeholder', plcHolder);
    });
    load_tags();


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

let compTa = new getTypeaheadOpt('company', companies, limit_sugg);

let refTa = new getTypeaheadOpt('reference', references, limit_sugg);

let countriesTa = new getTypeaheadOpt('country', countries, limit_sugg);

let tagsTa = new getTypeaheadOpt('tags', tags, limit_sugg);


let allTypeaheadDic = {
    'sust_tags': tagsTa,
    'company': compTa,
    'reference': refTa,
    'country': countriesTa,
    'tags_select': tagsTa,
};