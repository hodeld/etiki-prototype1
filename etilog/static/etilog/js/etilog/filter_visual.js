$(document).ready(function () {


});

let filterCount = 0;

function setFilterIcon() {
    const ele = $('#id_search')[0];
    const phbase = ele.dataset.phbase;
    let ph;
    if (filterCount <= 0) {
        filterCount = 0
        ph = ele.dataset.phsearch + phbase;
    } else {
        ph = ele.dataset.phfilter + phbase;
    }
    $('.filter-count').html(filterCount);
    $('.f_search:not(.tt-hint)').attr('placeholder', ph);
}

function setFilterVisually(filterDict) {
    submit = false;
    const nameSel = 'input[name ="{name}"]';
    const fform = $('#id_filterform');
    for (let el_name in filterDict) {
        let valList = filterDict[el_name];
        if (valList.length > 0) {

            fSel = nameSel.replace('{name}', el_name);
            ele = fform.find(fSel);
            var parfield = ele.attr('parfield');
            if (ele.hasClass('btninput')) {
                let newVal = JSON.stringify(valList);
                ele.val(newVal); //value set from filter is string incl. [
                $.each(valList, function (index, value) {
                    filterCount++;
                    const targetId = parfield + value;
                    $(targetId).attr('aria-pressed', 'true')
                        .addClass('active');
                    //needed as to buttons with different ID
                    if ($(targetId).attr('twin-id')) {
                        var twinId = '#' + $(targetId).attr('twin-id');
                        $(twinId).addClass('active')
                            .attr('aria-pressed', 'true');
                    }

                });
            } else if (ele.hasClass('f_tagsinput')) {
                $.each(valList, function (index, value) {
                    let suggestion = value; //filterDict[value] ;
                    setTags(suggestion, true); //includes filterCount
                });
                //let targetId = parfield;  //+ el_name; //eg company
                //$(targetId).addClass('show');
            } else if (ele.hasClass('f_dateinput')) {
                //sets value and filterCount
                $(parfield).data("DateTimePicker").date(valList);
            } else if (ele.hasClass('f_tagsinput_spec')) {
                $.each(valList, function (index, value) {
                    filterCount++;
                    let suggestion = value; //filterDict[value] ;
                    const tagInputEle = $('#id_f_reference_exc_tinp');
                    tagInputEle.tagsinput('add', suggestion); //sets also filtervalue
                });
            }

        }
    }
    setFilterIcon()
    submit = true;
}
