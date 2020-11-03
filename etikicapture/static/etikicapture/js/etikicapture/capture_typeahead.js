$(document).ready(function () {

        //used for fields in capture
    initTagInput();

    $('.c_tags_select').each(function () {
        let ele_name = $(this).attr('name');
        $(this).tagsinput({
            itemValue: 'id',
            itemText: 'name',
            itemCategory: 'category',
        });
        //placeholder automatically added

    });
    $('#id_tags_select').on('beforeItemRemove', function (event) {
        if (event.options) {
            return
        }
        const suggestion = event.item;
        //$('#id_sust_tags').tagsinput('add', suggestion, );
        $('#id_tags_drop').tagsinput('add', suggestion, );
    });

    $('#id_tags_drop').on('beforeItemRemove', function (event) {
        if (event.options) {
            return
        }
        const suggestion = event.item;
        $('#id_tags_select').tagsinput('add', suggestion, );
        let idVal = suggestion.id;
        setFormValue('#id_sust_tags', idVal, false);
    });
    $('#id_tags_drop').on('beforeItemAdd', function (event) {
        const suggestion = event.item;
        let idVal = suggestion.id;
        setFormValue('#id_sust_tags', idVal, true);
    });


    load_tags();


});

const limit_sugg = 5;

let compTa = new getTypeaheadOpt('company_all', limit_sugg);

let refTa = new getTypeaheadOpt('reference',  limit_sugg);

let countriesTa = new getTypeaheadOpt('country', limit_sugg);

let tagsTa = new getTypeaheadOpt('tags', limit_sugg);

let tagsFSource = localBH();
let tagsFTa = new getTypeaheadOpt('tagsF', limit_sugg, tagsFSource);


let allTypeaheadDic = {
    //'sust_tags': tagsFTa,

    'company': compTa,
    'reference': refTa,
    'country': countriesTa,

    'tags_select': tagsTa,
    'tags_drop': tagsFTa,

    'owner': compTa,
    'subsidiary': compTa,
    'supplier': compTa,
    'recipient': compTa,
};

const maxTagsDic = {
    //'sust_tags': tagsFTa,
    'company': 1,
    'reference': 1,
    'country': 1,
    //'tags_select': tagsTa,
};

function load_tags() {
    $('#id_tags_drop').tagsinput('removeAll');
    $('#id_sust_tags').val('');

    let url = load_tags_f;
    var domainId = $("#id_sust_domain").val(); // get the selected Domain ID
    var categoryId = $("#id_sust_tendency").val(); // get the selected tendency ID
    $.ajax({ // initialize an AJAX request
        url: url, // set the url of the request (= '')
        data: {
            // both can be null
            'domainId': domainId,
            'categoryId': categoryId

            // add the domainId to the GET parameters
        },
        success: function (data) { // `data` is the return of the
            // id_tags_select
            tagsFSource.local = data;
            tagsFSource.initialize(true);
            $('#id_tags_select').tagsinput('removeAll',{preventContinue:true});

            $.each(data, function (index, tag) {
                $('#id_tags_select').tagsinput('add', tag);
            });

            //add click event on all tags
            $('.div_tags_select .bootstrap-tagsinput .badge').click(function (event) {
                const $ele = $(event.target);
                const tag = $ele.data('item');
                $('#id_tags_select').tagsinput('remove', tag);

            });

            //$("#id_sust_tags").html(data); // replace the
        }

    });
}


function initTagInput(parentID=''){
    $(parentID + ' ' + '.c_tags_search_inp').each(function () {
        let ele_name = $(this).attr('name');
        let optDic = allTypeaheadDic[ele_name];
        let typeAJS = [];
        if (Array.isArray(optDic)){
            typeAJS = [
                {
                    highlight: true,
                    autoselect: true,
                },
                    ...optDic,
            ];
        }
        else {
            typeAJS = [
                {
                    highlight: true,
                    autoselect: true,
                },
                optDic,
            ]
        }
        const maxTags = maxTagsDic[ele_name]  || undefined;
        $(this).tagsinput({
            itemValue: 'id',
            itemText: 'name',
            itemCategory: 'category',
            maxTags: maxTags,
            typeaheadjs: typeAJS,
        });
    });
}

function localBH(lSource){

    let tagsFOpts = {
            datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'), //obj.whitespace('name') -> data needs to be transformed
            queryTokenizer: Bloodhound.tokenizers.whitespace,
            //identify: function(obj) { return obj.id; }, //to get suggestion by ID -> not used and breaks typahead!
            local: [],
        };

    let bHSource = new Bloodhound(tagsFOpts);
    return bHSource


}