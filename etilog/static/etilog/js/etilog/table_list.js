$(document).ready(function () {


});


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