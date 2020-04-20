$(document).ready(function () {
    //button select for categories
    //$('.btnselect').on('click', mirror_btn);

    //send element as with event.target it can be fa-icon!
    $('.btnselect').click(function () {
        set_val_from_btn($(this))
    });

    $('#filterClear').click(function () {
        clearFilter()
    });


    // pass options to ajaxForm
    //$('#id_filterform').ajaxForm(options);


    $('#applyFilter').click(function () {
        resultType = 'table';
        submitFromID('#id_filterform');
    });

    //directly submit on filterinputs:
    $('.f_input').change(function (ev) {
        submitFilterForm(ev)
    });

    //directly submit on datetimeinput
    $(".dateyearpicker").on('dp.change', function (ev) { // e = event
        submitFilterForm(ev)
    });


    var multitemplate_st = '<h5 class="category-name text-primary">';
    var multitemplate_et = '</h5>';
    var limit_sugg = 3;

    //add tagsinput and typeahead on hidden fields
    $('.f_tagsinput').each(function () {
        var ele_name = $(this).attr('name');
        var optDic = allTypeaheadDic[ele_name];
        if (optDic) {
            $(this).tagsinput({
                itemValue: 'id',
                itemText: 'name',
                typeaheadjs: [
                    {
                        highlight: true,
                        autoselect: true,
                    },
                    optDic,
                ],
            });
            var plcHolder = $(this).attr('placeholder');

            var parentId = $(this).attr('parfield');
            $(parentId).find('.bootstrap-tagsinput input.tt-input').attr('placeholder', plcHolder);

        }
        ;
    });

    $(".f_tagsinput").keyup(function (event) {
        var ele = $(this);
        keyBehaviorSearch(event, ele);
    });

    $('.f_tagsinput').on('itemRemoved', function (event) {
        if ($(this).tagsinput('items').length == 0) {
            var parentId = $(this).attr('parfield');
            $(parentId).removeClass('show');
        }

    });


    //initialize typehead -> needs to be below source (assignment is in order in js!
    $('#id_search').typeahead(
        ...allTaHList //elements of list
    );

    $('#id_search').bind('typeahead:select', function (ev, suggestion) {

        //from search directly table
        resultType = 'table';

        var val_str = suggestion['name'];
        var val_id = suggestion['id'];


        if (val_str.length > 0) {
            var modname = ev.handleObj.handler.arguments[2];
            if (modname == 'companies') {
                var elt = $('#id_f_company');
            } else if (modname == 'countries') {
                var elt = $('#id_f_country');
            } else if (modname == 'references') {
                var elt = $('#id_f_reference');
            } else if (modname == 'tags') {
                var elt = $('#id_f_tags');
            } else {
                var elt = $('#id_f_freetext');
            }

            setTags(elt, suggestion);
            $(this).typeahead('val', ''); //typeahead input
        }


    });


    $('.topic-link').click(function () {
        var tagname = $(this).attr('tagname');
        var tagid = parseInt($(this).attr('tagid'));
        resultType = 'table';
        set_tag(tagid, tagname)

    });

    $("#id_search").keyup(function (event) {
        var ele = $(this);
        keyBehaviorSearch(event, ele);
    });

});


var drawcharts = false;

function mirror_btn(ele) {
    var twin_id = '#' + ele.attr('twin-id');
    var twin_ele = $(twin_id);
    var pressed = ele.attr('aria-pressed'); // jquery: true or fals

    if (pressed == "false") { //means was not pressed
        twin_ele.attr('aria-pressed', 'true');
        twin_ele.addClass('active');
    } else {
        twin_ele.attr('aria-pressed', 'false');
        twin_ele.removeClass('active');
    }
}


function set_val_from_btn(ele) {
    mirror_btn(ele);
    var el_id = ele.attr('id');
    var id_val = Number(ele.attr('name'));
    var input_id = '#' + ele.attr('targfield');
    var pressed = ele.attr('aria-pressed'); // true or false

    var el_val = $(input_id).val();
    try {
        var val_set = new Set(JSON.parse("[" + el_val + "]"));
    } catch (err) {
        console.log(err.message);
    }


    if (pressed == "false") { //means was pressed now
        val_set.add(id_val);
    } else {
        val_set.delete(id_val);
    }
    new_li = Array.from(val_set);
    if (ele.hasClass('gettable')) {
        resultType = 'table';
    }

    $(input_id).val(new_li)
        .trigger('change'); //needed for hidden input fields
}

function prepare_list() {
    $('tbody').addClass("list"); // for list filter
    $('.table-container').attr('id', 'impev-list'); // for list filter
    //need to be in same container as table for list filter
    //$('.table-container').prepend('<input  class="search form-control" placeholder="Search"  />');

    $('.table-container').append('<nav aria-label="Table navigation"><ul class="pagination justify-content-center"></ul></nav>')

    var impevopts = {
        valueNames: ['company', 'country', 'reference', 'sust_domain', 'topics',
            'date', 'date_sort', 'reference_sort', 'sudom_sort',
            'id'],
        page: 20,
        pagination: {
            innerWindow: 2,
            outerWindow: 1,
            left: 0,
            right: 0,
            paginationClass: "pagination", //class name generated in django-table
        }
    };

    //initiate List incl. pagination
    var impevList = new List('impev-list', impevopts);
    //searchfield outside container:
    $('#id_search').on('keyup', function () {
        var searchString = $(this).val();
        impevList.search(searchString);
    });
    $('#id_search').bind('typeahead:select', function () {
        impevList.search(''); //to clear List search
    });
    impevList.sort('date_sort', {order: "desc"});
    impevList.sort('company', {order: "asc"});
    //impevList.sort('date_sort', { order: "desc" }); //as to start
}


function set_filterbtns_notused() {
    $.each(btns_dict, function (k, v) {
        var part_id = '#id-' + k + '-btn-';	//k = sust_domain or sust_tendency
        $.each(v, function (index, val_i) {
            var btn_id = part_id + val_i;
            //$(btn_id).addClass("active");
            $(btn_id).click(); //clicks and adds to hidden input
        });
    });
}

function toggle_visibility(jqid) {
    var e = $(jqid);
    if (e.hasClass('show')) {
        e.removeClass('show');
    } else {
        e.addClass('show');
    }
}

//set tags from topics
function set_tag(id, tagname) {
    var suggestion = {'id': id, 'name': tagname};
    var ele = $('#id_f_tags');
    setTags(ele, suggestion);

}


var ie_details = '';
var comp_ratings = '';
var resultMessage = '';

function setData(response) {
    var responseType = response.result_type;
    $('#filterCountText').html(response.msg_count);
    if (responseType === 'count') {
        $("#id_message").html(resultMessage);
        return
    }
    var tblData = response.table_data;
    var compData = response.comp_details;
    var msg = response.message;

    ie_details = JSON.parse(response.ie_details);
    comp_ratings = JSON.parse(response.comp_ratings);
    resultMessage = msg;
    $("#id_message").html(msg);

    drawcharts = true;
    //when google is loaded
    google.charts.setOnLoadCallback(drawCharts);

    $("#company-details-row").html(compData);
    $("#id_ovtable").html(tblData);

    set_topheadaer();//new th elements
    prepare_list();

}

var resultType = 'count';
//form ajax options
var formOptions = {

    beforeSubmit: function (arr, $form, options) {
        $("#id_message").html('calculating results …');
        setFilterIcon();
        if (landing == true) { //means was pressed now
            startanimation(); // only first time when table is hidden
        }
        var form = $form //$('#id_filterform');
        var acturl = form.serialize(); //

        var searchurl = list_url + 'search?' + acturl; //list_url: etilog:home
        window.history.pushState("", "", searchurl); //TODO direct url search


    },
    success: function (response) {
        setData(response)
        resultType = 'count';

    },
    url: list_url, //needed to be defined due to searchurl


};


function submitFilterForm(ev) {
    var target = $(ev.target);
    if (target.hasClass('nosubmit')) {
        target.removeClass('nosubmit');
    } else {

        var foid = '#' + ev.target.form.id;
        submitFromID(foid);
    }
}

function submitFromID(foid) {
    //manipulate extra data
    formOptions.data = {result_type: resultType}
    $(foid).ajaxSubmit(formOptions)

}

function setFilterIcon() {
    var validate = false;
    var filterCount = 0;
    $('.f_input').each(function () {
        if ($(this).val() != '') {
            filterCount++;
            validate = true;
        }

    });
    if (!validate) {

        $('#icon_filter_active').hide();
        $('#icon_filter').show();
    } else {
        $('#icon_filter').hide();
        $('#icon_filter_active').show();
        var $el = $('#applyFilter'),
            originalColor = $el.css("background");

        $el.attr('style', "background: #ffff99 !important"); //due to mdb
        setTimeout(function () {
            $el.animate({
                backgroundColor: originalColor
            }, 100, function () {
                $el.removeAttr('style');
            });
        }, 200);

    }
    $('#filter-count').html(filterCount);
}

function setFilterVisually(filterDict) {
    var filterCount = 0;
    $('.f_input').each(function () {

        var ele = $(this);
        if (ele.val() != '') {
            filterCount++;
            var val = ele.val();
            var parfield = ele.attr('parfield');
            var el_name = ele.attr('name');
            var valList = filterDict[el_name];
            if (ele.hasClass('btninput')) {
                ele.val(valList); //value set from filter is string incl. [
                $.each(valList, function (index, value) {
                    //todo check but should only ids
                    var targetId = parfield + value;
                    $(targetId).attr('aria-pressed', 'true')
                        .addClass('active');
                    if ($(targetId).attr('twin-id')) {
                        var twinId = '#' + $(targetId).attr('twin-id');
                        $(twinId).addClass('active')
                            .attr('aria-pressed', 'true');
                    }


                });
            } else if (ele.hasClass('f_tagsinput')) {
                function addTag(suggestion) {
                    ele.addClass('nosubmit');
                    ele.tagsinput('add', suggestion);
                }

                var targetId = parfield //+ el_name; //eg company
                if (el_name == 'summary') {
                    addTag(val)
                } else {

                    $.each(valList, function (index, value) {
                        var suggestion = value; //filterDict[value] ;
                        addTag(suggestion)
                    });
                }
                $(targetId).addClass('show');
            } else if (ele.hasClass('dateyearpicker')) {

                //ele.data("DateTimePicker").date(val);

            }

            $('#icon_filter').hide();
            $('#icon_filter_active').show();

        }
    });
    $('#filter-count').html(filterCount);
}

function clearFilter() {
    var filterCount = 0;
    $('.f_tagsinput').each(function () {

        var ele = $(this);
        if (ele.val() != '') {
            ele.addClass('nosubmit');
            ele.tagsinput('removeAll');
        }
    });

    $('.btnselect').attr('aria-pressed', 'false');
    $('.btnselect').removeClass('active');
    $('.row_tags_class').hide();

    $('.f_input').each(function () {

        var ele = $(this);
        if (ele.val() != '') {
            ele.addClass('nosubmit');
            ele.val('');
        }
    });
    resultType = 'count';

    submitFromID('#id_filterform');

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

function keyBehavior(event, ele) {
    if (event.keyCode === 13) { //enter
        setFirstSelection(ele);
        ele.blur();
        ele.focus();
    }
    ;
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

function setTags(ele, suggestion) {
    ele.tagsinput('add', suggestion);	//adds tag
    parentId = ele.attr('parfield');
    $(parentId).addClass('show');
}

function setTagBtn(eleId) {
    var ele = $('#' + eleId);
    if (setFirstSelection(ele) === false) {
        changeWOSelection(ele);
    }
    ;
}

function setFirstSelection(ele) {
    var firstsel = ele.parent().find('.tt-selectable:first');
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
