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
        var ele = $(this);
        keyBehaviorSearch(event, ele);
    });
});


//on search button in searchfield
function setTagBtn(eleId) {
    const ele = $('#' + eleId);
    if (setFirstSelection(ele) === false) {
        changeWOSelection(ele);
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
    let suggestion = {
            'id': val_str,
            'name': val_str,
            'category': 'summary'
        };
    setTags(suggestion);
    ele.typeahead('val', ''); //typeahead input
    ele.focus();
}


function keyBehaviorSearch(event, ele) {
    if (event.keyCode === 13) { //enter
        if (ele.val()!== '') {
            changeWOSelection(ele);
        }
    }
}

//initialize BLOODHOUND
function getBloodhoundOpt(field_url) {
    optDict = {
        datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'), //obj.whitespace('name') -> data needs to be transformed
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        //identify: function(obj) { return obj.id; }, //to get suggestion by ID -> not used and breaks typahead!
        prefetch: {
            url: field_url, // url set in html
            cache: true	 // defaults to true -> for testing
        },
    };
    return optDict
}

var bldhndOptComp = new getBloodhoundOpt(companies_url);
var companies = new Bloodhound(bldhndOptComp);

var optCountries = new getBloodhoundOpt(countries_url);
var countries = new Bloodhound(optCountries);

var optReferences = new getBloodhoundOpt(references_url);
var references = new Bloodhound(optReferences);

var optTopics = new getBloodhoundOpt(tags_url);
var tags = new Bloodhound(optTopics);


//typeahead
var multitemplate_st = '<h5 class="category-name text-primary">';
var multitemplate_et = '</h5>';
var limit_sugg = 3;

function getTypeaheadOpt(name, source) {
    const optDict = {
        name: name,
        source: source,
        display: 'name',
        limit: limit_sugg,
    };
    return optDict
}

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

var compTa = new getTypeaheadOpt('company', companies);
var compTaH = new tAwHeaderOpt(compTa, 'Companies');

var refTa = new getTypeaheadOpt('reference', references);
var refTaH = new tAwHeaderOpt(refTa, 'Where was it published');

var countriesTa = new getTypeaheadOpt('country', countries);
var countriesTaH = new tAwHeaderOpt(countriesTa, 'Countries');

var tagsTa = new getTypeaheadOpt('tags', tags);
var tagsTaH = new tAwHeaderOpt(tagsTa, 'Topics');

var allTypeaheadDic = {
    'tags': tagsTa,
    'company': compTa,
    'reference': refTa,
    'country': countriesTa,
};

var allTaHList = [
    {
        highlight: true,
        autoselect: true,  //highlights and selects on enter
    },
    compTaH, countriesTaH, refTaH,
    tagsTaH
];