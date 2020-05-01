$(document).ready(function () {

    $(".f_tagsinput").keyup(function (event) {
            var ele = $(this);
            keyBehaviorSearch(event, ele);
        });
});

function keyBehavior(event, ele) {
    if (event.keyCode === 13) { //enter
        setFirstSelection(ele);
        ele.blur();
        ele.focus();
    }
    ;
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

    var eletarget = $('#id_f_summary');
    var el_id = '#id_row_f_summary';

    var val_str = ele.typeahead('val');

    eletarget.tagsinput('add', val_str);	//adds tag
    $(el_id).show();
    ele.typeahead('val', ''); //typeahead input
    ele.focus();

}


function keyBehaviorSearch(event, ele) {
    if (event.keyCode === 13) { //enter
        setFirstSelection(ele);
        if (setFirstSelection(ele) === false) {
            changeWOSelection(ele);
        }
        ;
    }
    ;
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
    }
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
    optDict = {
        name: name,
        source: source,
        display: 'name',
        limit: limit_sugg,
    }
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

var compTa = new getTypeaheadOpt('companies', companies);
var compTaH = new tAwHeaderOpt(compTa, 'Companies');

var refTa = new getTypeaheadOpt('references', references);
var refTaH = new tAwHeaderOpt(refTa, 'Where was it published');

var countriesTa = new getTypeaheadOpt('countries', countries);
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
        autoselect: true,
    },
    compTaH, countriesTaH, refTaH,
    tagsTaH
];