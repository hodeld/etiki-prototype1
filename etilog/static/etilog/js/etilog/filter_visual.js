$(document).ready(function () {


});


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
