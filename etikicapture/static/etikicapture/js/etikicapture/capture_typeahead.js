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
        });
        let plcHolder = $(this).attr('placeholder');
        let parentId = $(this).attr('parfield');
        $(parentId).find('.bootstrap-tagsinput input.tt-input').attr('placeholder', plcHolder);
    });
    $('#id_c_tags_select').on('beforeItemRemove', function (event) {
        if (event.options) {
            return
        }
        const suggestion = event.item;
        $('#id_c_sust_tags').tagsinput('add', suggestion, );
    });

    $('#id_c_sust_tags').on('beforeItemRemove', function (event) {
        if (event.options) {
            return
        }
        const suggestion = event.item;
        $('#id_c_tags_select').tagsinput('add', suggestion, );
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

var tagsFData = [{id: 15, name: "Animal Testing"}, {id: 16, name: "Factory Farming"}];

let tagsFOpts = {
        datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'), //obj.whitespace('name') -> data needs to be transformed
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        //identify: function(obj) { return obj.id; }, //to get suggestion by ID -> not used and breaks typahead!
        local: tagsFData,
    };

let tagsFSource = new Bloodhound(tagsFOpts);
let tagsFTa = new getTypeaheadOpt('tagsF', tagsFSource, limit_sugg);


let allTypeaheadDic = {
    'sust_tags': tagsFTa,
    'company': compTa,
    'reference': refTa,
    'country': countriesTa,
    'tags_select': tagsTa,
};


function load_tags() {
    //let url = $("#id_sust_tags").attr("data-url"); // get
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
            // id_c_tags_select
            tagsFSource.local = data;
            tagsFSource.initialize(true);
            $('#id_c_tags_select').tagsinput('removeAll',{preventContinue:true});

            $.each(data, function (index, tag) {
                $('#id_c_tags_select').tagsinput('add', tag);
            });
            //$("#id_sust_tags").html(data); // replace the
        }

    });
}

function selectTag(ele){
    console.log();
};