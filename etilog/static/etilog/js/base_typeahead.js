$(document).ready(function () {

});

//initialize BLOODHOUND
function getBloodhoundOpt(name, field_url, remote=false, caching=false) {

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
        //returned value needs to be unique -> name in front
        identify: function(obj) { return name + obj.id.toString(); },

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


const paramDict  = {
    'company': [companies_url, true],
    'country': [countries_url, false],
    'reference': [references_url, false],
    'tags': [tags_url, false],
    'industry': [industry_url, false],
    'company_all': [companies_all_url, true],
    'reference_exc': [references_url, false],
};

//TypeaheadOpt
function getTypeaheadOpt(name, limitSugg=3, source=undefined) {
    if (source === undefined) {
        let params = paramDict[name];
        let objUrl = params[0],
            rem = params[1];
        let objOPtions = new getBloodhoundOpt(name, objUrl, rem);
        source = new Bloodhound(objOPtions);
    }

    const optDict = {
        name: name,
        source: source,
        display: 'name',
        limit: limitSugg,
    };
    return optDict
}