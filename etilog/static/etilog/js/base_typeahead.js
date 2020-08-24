$(document).ready(function () {

});

//initialize BLOODHOUND
function getBloodhoundOpt(field_url, caching=true) {
    optDict = {
        datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'), //obj.whitespace('name') -> data needs to be transformed
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        //identify: function(obj) { return obj.id; }, //to get suggestion by ID -> not used and breaks typahead!
        prefetch: {
            url: field_url, // url set in html
            cache: caching, // false if new added items should be shown
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

//TypeaheadOpt
function getTypeaheadOpt(name, source, limitSugg=3) {
    const optDict = {
        name: name,
        source: source,
        display: 'name',
        limit: limitSugg,
    };
    return optDict
}