$(document).ready(function () {

});

//initialize BLOODHOUND
function getBloodhoundOpt(field_url, remote=false, caching=false) {

    optDict = {
        datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'), //obj.whitespace('name') -> data needs to be transformed
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        //identify: function(obj) { return obj.id; }, //to get suggestion by ID -> not used and breaks typahead!
        prefetch: {
            url: field_url, // url set in html
            cache: caching, // false if new added items should be shown.
                            // if true even hard reload does not reload
                            // could probably be done with bloodHound.clearPrefetchCache();
        },
        identify: function(obj) { return obj.id; },

    };
    if (remote){
        //if results < sufficient -> remote
        const wildcard = '%QUERY'
        optDict.remote = {
            url: field_url + '/' + wildcard,
            wildcard: wildcard,
        }
        optDict.sufficient = 3
    }
    return optDict
}

var bldhndOptComp = new getBloodhoundOpt(companies_url, true);
var companies = new Bloodhound(bldhndOptComp);


let OptIndustry = new getBloodhoundOpt(industry_url);
let industries = new Bloodhound(OptIndustry);

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