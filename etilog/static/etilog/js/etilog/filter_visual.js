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
    let filterCount = 0;
    const nameSel = 'input[name ="{name}"]';
    const fform = $('#id_filterform');
    for (let el_name in filterDict) {
        let valList = filterDict[el_name];
        if (valList.length > 0) {
            filterCount++;
            fSel = nameSel.replace('{name}', el_name);
            ele =  fform.find(fSel);
            var parfield = ele.attr('parfield');
            ele.addClass('nosubmit');
            if (ele.hasClass('btninput')) {
                let newVal = JSON.stringify(valList);
                ele.val(newVal); //value set from filter is string incl. [
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


                $.each(valList, function (index, value) {
                        let suggestion = value; //filterDict[value] ;
                        ele.addClass('nosubmit');
                        setTags(suggestion, true);
                    });
                //let targetId = parfield;  //+ el_name; //eg company
                //$(targetId).addClass('show');
            } else if (ele.hasClass('dateyearpicker')) {
                ele.data("DateTimePicker").date(valList);
            }

            $('#icon_filter').hide();
            $('#icon_filter_active').show();

        }
    }
    $('#filter-count').html(filterCount);
}
