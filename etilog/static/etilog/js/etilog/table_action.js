$(document).ready(function () {


    $('.trshowdetails').click(function () {
        toggle_filter()
    });


});

function toggle_details(event, ele, ie_id) {
    const target = $(event.target);
    if (target.is("button") || target.is("a")) {
        return false;
    } else {
        const parele = $(ele).parent(); //original row
        if (parele.hasClass('active')){
            hide_details();
        }
        else {
            show_details(ele, ie_id);
        }
        //toggle_article(event);
    }
}

function hide_details() {
    $('.detailrow').removeClass('show');  //hide all detail rows
    $('.parentrow').removeClass('active'); //show all parent rows
}


//used in table on detail column
function show_details(parele, ie_id) {
    var rowid = ie_id + '_row';
    var detail_id = rowid + '_detail';
    if ($(parele).hasClass('parentrow')){
        $(parele).addClass('active')
        $('#' + detail_id).addClass('show');
    }
    else {
         getDetail(ie_id);
    }

}

let ie_details = '';

const detailOptions = {
    success: function (response) {
        setDetail(response)

    },
    url: result_url,

};

function getDetail(ie_id){
    detailOptions.data = {
        ie_id: ie_id,
        result_type: 'ie_detail'
    };
    $.ajax(detailOptions); // ajax request without form submit
    return
}

function setDetail(response){
    ie_details =  JSON.parse(response.ie_details);

    const ie_id = response.ie_id;
    const rowid = ie_id + '_row';
    const detail_id = rowid + '_detail';
    const parele = $('#' + rowid);
    const tableid = '#impev-list';
    $(parele).addClass('parentrow active')

    var colcnt = numOfVisibleCols(tableid);
    var rowstr1 = 'tr scope="row" class="detailrow darkbg collapse show" id="%%detailid" ';
    var rowstr3 = '<td colspan = "%%colcnt" > %%htmlstr </td> ';
    const rowstr4 = ' <td class=" details td-normal" onclick="hide_details();"></td> ';
    var rowstr = '<' + rowstr1 + '>' + rowstr3 + rowstr4 + '</tr>';
    var html_str = ie_details[ie_id][0];
    rowstr = rowstr.replace("%%htmlstr", html_str);
    rowstr = rowstr.replace("%%colcnt", colcnt - 1);
    rowstr = rowstr.replace("%%detailid", detail_id);

    $(parele).removeClass('show');
    $(parele).after(rowstr);


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

function numOfVisibleCols(tableid) {


    var colcnt = $(tableid).find('th').filter(function () { //find as not directly children
        return $(this).css('display') !== 'none';
    }).length;

    return colcnt
}
