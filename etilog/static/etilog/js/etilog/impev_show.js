/**
 *
 */

// jquery
$(document).ready(function () {
    hide_img_vid();

});


function hide_img_vid() {
    var articleid = '#id_articleshow ';
    $(articleid + 'img').hide();
    var vidtags = [articleid + "iframe", articleid + "video"];
    vidtags.forEach(function (item, index) { //to hide videos
        $(item).each(function (index) {
            $(this).parent().hide();
        });
    });

}