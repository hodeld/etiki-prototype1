
$(document).ready(function () {


});

const voteRelOptions = {
    success: function (response) {
        setVote(response)

    },
};

function voteRelevance(ele, vote){
    const $ele = $(ele);
    const par = $ele.parent();
    const ieId = par.attr('data-ie-id');
    const txtDiv = par.find('.text-vote');
    let voteC = parseInt(txtDiv.attr('data-value'));
    voteC = voteC + vote
    if (voteC < 1){
            voteC = 0
        }
    txtDiv.html(voteC);
    const url = vote_relevance;
    let voteOpts = {...voteRelOptions};
    voteOpts.data = {ie_id: ieId,
    vote: vote}
    $.ajax(url, voteOpts);

}

function setVote(response){
    const $ele = $('#vote_text' + response.ie_id);
    const voteC = response.vote_count;
    $ele.attr('data-value', voteC);
    $ele.html(voteC);

}