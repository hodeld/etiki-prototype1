$(document).ready(function () {

});

//initialize BLOODHOUND
function getBloodhoundOpt(field_url, reload=false) {
    optDict = {
        datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'), //obj.whitespace('name') -> data needs to be transformed
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        //identify: function(obj) { return obj.id; }, //to get suggestion by ID -> not used and breaks typahead!
        prefetch: {
            url: field_url, // url set in html
            cache: reload === true ? false : true, // false if new added items should be shown.
                            // if true even hard reload does not reload
                            // could probably be done with bloodHound.clearPrefetchCache();

        },
    };
    return optDict
}

var bldhndOptComp = new getBloodhoundOpt(companies_url, companyReload);
var companies = new Bloodhound(bldhndOptComp);

let OptIndustry = new getBloodhoundOpt(industry_url);
let industries = new Bloodhound(OptIndustry);

var optCountries = new getBloodhoundOpt(countries_url);
var countries = new Bloodhound(optCountries);

var optReferences = new getBloodhoundOpt(references_url, referenceReload);
var references = new Bloodhound(optReferences);

var optTopics = new getBloodhoundOpt(tags_url, tagsRelaod);
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