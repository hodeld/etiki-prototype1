$(document).ready(function () {

    //initialize typehead -> needs to be below source (assignment is in order in js!
    $('.f_search').typeahead(
        ...allTaHList //elements of list
    );
    $('.f_search').bind('typeahead:select', function (ev, suggestion) {
        //from search directly table
        const val_str = suggestion['name'];
        if (val_str.length > 0) {
            const category = ev.handleObj.handler.arguments[2];
            suggestion.category = category;
            setTags(suggestion);
            $(this).typeahead('val', ''); //typeahead input
        }
    });

    $(".f_search").keyup(function (event) {
        const ele = $(this);
        keyBehaviorSearch(event, ele);
    });


    $('.f_tags_search_inp').typeahead(
        {
            highlight: true,
            autoselect: true,
        },
        refExcTa,
    );

    $('.f_tags_search_inp').bind('typeahead:select', function (ev, suggestion) {
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


//on search button in searchfield
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


//typeahead
var multitemplate_st = '<h5 class="category-name text-primary">';
var multitemplate_et = '</h5>';
const limit_sugg = 3;


function tAwHeaderOpt(optDict, title) {
    var templatesDic = {
        templates: {
            header: multitemplate_st + title + multitemplate_et
        }
    };
    //combines 2 dics
    var newOptDict = {...optDict, ...templatesDic};
    return newOptDict
}

var compTa = new getTypeaheadOpt('company', companies, limit_sugg);
var compTaH = new tAwHeaderOpt(compTa, 'Companies');

var refTa = new getTypeaheadOpt('reference', references, limit_sugg);
var refTaH = new tAwHeaderOpt(refTa, 'Where was it published');

var countriesTa = new getTypeaheadOpt('country', countries, limit_sugg);
var countriesTaH = new tAwHeaderOpt(countriesTa, 'Countries');

var tagsTa = new getTypeaheadOpt('tags', tags, limit_sugg);
var tagsTaH = new tAwHeaderOpt(tagsTa, 'Topics');

let refExcTa = new getTypeaheadOpt('reference_exc', references, 5);



var allTaHList = [
    {
        highlight: true,
        autoselect: true,  //highlights and selects on enter
    },
    compTaH, countriesTaH, refTaH,
    tagsTaH
];