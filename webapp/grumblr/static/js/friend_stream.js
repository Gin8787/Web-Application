function populateList() {
console.log("In profile populateList");
var list = $("#post-list");
var username = list.attr("name")
console.log("username is ")
console.log(username)
$.get("/grumblr/get_posts_friend/" + username)
    .done(function(data) {
        console.log("In populateList done")

        list.data('max-time', data['max-time']);
        list.html('')
        for (var i = 0; i < data.posts.length; i++) {
            post = data.posts[i];
            var new_post = $(post.html);
            console.log(new_post);
            new_post.data("post-id", post.id);
            list.append(new_post);

            getComments(post.id);

        }
    });
}

function addComment() {
    console.log("In addComment");
    var post = $(this).parent().parent().parent().parent();
    var post_id = post.attr('id')
    console.log(post);
    console.log(post_id);
    var commentField = $("#comment-field" + post_id);
    $.post(("/grumblr/add_comment/" + post_id), {"comment": commentField.val()})
        .done(function(data) {
            console.log("In addComment done")
            var list_comment = $("#comment-list" + post_id);
            var new_comment = $(data.html);
            console.log(list_comment)
            list_comment.append(new_comment);
            commentField.val("").focus();
        });
}

function getComments(id) {
    var list_comment = $("#comment-list" + id);
    $.get(("/grumblr/get_comments/" + id))
    .done(function(data) {

        for(var i = 0; i < data.comments.length; i++ ) {
            var comment = data.comments[i];
            var new_comment = $(comment.html);
            list_comment.append(new_comment);
        }
    })
}

$(document).ready(function() {
    console.log("In ready");
    $("#post-list").on("click", "button", addComment);

    populateList();
    $("#post-field").focus();


    function getCookie(name) {
        var cookieValue = null;
        if(document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if(cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });
});