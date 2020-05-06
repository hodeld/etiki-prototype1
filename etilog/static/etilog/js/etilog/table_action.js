$(document).ready(function () {


    $('.trshowdetails').click(function () {
        toggle_filter()
    });


});

function numOfVisibleCols(tableid) {


    var colcnt = $(tableid).find('th').filter(function () { //find as not directly children
        return $(this).css('display') !== 'none';
    }).length;

    return colcnt
}

//used in table on detail column
function show_details(ele, ie_id, event) {
    if (toggle_details(event) == false) {
        return;
    }
    var tableid = '#impev-list';
    var parele = $(ele).parent(); //original row
    var rowid = ie_id + '_row';
    var detail_id = rowid + '_detail';
    $(parele).addClass('parentrow')

    var colcnt = numOfVisibleCols(tableid);
    var rowstr1 = 'tr scope="row" class="detailrow darkbg" id="%%detailid" ';
    var rowstr3 = '<td colspan = "%%colcnt" > %%htmlstr </td> ';
    const rowstr4 = ' <td class=" details td-normal" onclick="toggle_details(event)"><i class="fas fa-chevron-up"></i></td> ';
    var rowstr = '<' + rowstr1 + '>' + rowstr3 + rowstr4 + '</tr>';
    var html_str = ie_details[ie_id][0];
    rowstr = rowstr.replace("%%htmlstr", html_str);
    rowstr = rowstr.replace("%%colcnt", colcnt - 1);
    rowstr = rowstr.replace("%%detailid", detail_id);
    
    $(parele).hide();
    $(parele).after(rowstr);


}

function toggle_details(event) {
    var target = $(event.target);
    if (target.is("button") || target.is("a")) {
        return false;
    } else {
        $('.detailrow').hide(); //oder open will be hidden
        $('.parentrow').show(); //oder open will be hidden
        //toggle_article(event);
    }

}

function full_article(ele, ie_id) {
    var html_str = ie_details[ie_id][2]; //article row

    $('#fullArticleContent').html(html_str);
    hide_img_vid();
    $('#modalFullArticle').modal('toggle');
}


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