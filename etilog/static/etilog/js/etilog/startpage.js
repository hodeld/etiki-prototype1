/**
 *
 */

// jquery
$(document).ready(function () {


    $(window).resize(function () { //window changes-> a lot need to be handled
        var timeout = false, // holder for timeout id
            delay = 400; // delay after event is "complete" to run callback
        // clear the timeout
        clearTimeout(timeout);
        // start timing for event "completion"
        timeout = setTimeout(set_topheadaer, delay);
    });

    var prevScrollTop = $(window).scrollTop()

    $(window).on('scroll', function (e) {

        var currentScrollTop = $(this).scrollTop()
        var ele = $('#divFilterBar')
        //on scrolling up: sticky-top
        if (currentScrollTop >= prevScrollTop) {
            ele.removeClass('sticky-top');
            ele.css({top: ''});
        } else {
            let hNavbar = $('#id_contsearch').outerHeight(); //smaller than navbar id_navbar
            ele.addClass('sticky-top');
            ele.css({top: hNavbar});
        }


        prevScrollTop = currentScrollTop
    });
    $('.tooltip-item').tooltip({trigger : 'hover'});

    if (landing == false) {
        startsettings();
    }

});

function startsettings() {
    var filterDict = JSON.parse(jsData.filter_dict);
    setFilterVisually(filterDict);
    setData(jsData);
    scrollToEle();

}

function startanimation() {
    // call when first time landing
    $('.landing').removeClass('landing');
    scrollToEle();
}


function scrollToEle(eleId = '#tabContent') {
    let hi = $('#id_contsearch').outerHeight(); //smaller than navbar id_navbar
    $([document.documentElement, document.body]).animate({
        scrollTop: $(eleId).offset().top - hi
    }, 2000);

}

function set_topheadaer() {
    let hNavbar = $('#id_contsearch').outerHeight(); //smaller than navbar id_navbar
    let hFilter = $('#divFilterBar').outerHeight(); //smaller than navbar id_navbar
    let hTotal = hNavbar; //+  hFilter;
    //$('#divFilterBar').css({ top: hNavbar });
    $('.table-etiki th').css({top: hTotal});
}
	
