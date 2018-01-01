function populateList() {
console.log("In populateList");
$.get("/grumblr/get_posts")
    .done(function(data) {
        console.log("In populateList done")
        var list = $("#post-list");
        list.data('max-time', data['max-time']);
        list.html('')
        for (var i = 0; i < data.posts.length; i++) {
            post = data.posts[i];
            var new_post = $(post.html);
            console.log(new_post);
            new_post.data("post-id", post.id);
            list.prepend(new_post);

            getComments(post.id);

        }
    });
}

function addPost() {
    console.log("In addPost");
    var postField = $("#post-field");
    console.log(postField);
    console.log(postField.val());
    $.post("/grumblr/postMsg", {"post": postField.val()})
        .done(function(data) {
            getUpdates();
            postField.val("").focus();
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

function getUpdates() {
    console.log("In getUpdates");
    var list = $("#post-list")
    var max_time = list.data("max-time")
    $.get(("/grumblr/get_changes/" + max_time))
        .done(function(data) {
            list.data('max-time', data['max-time']);
            for (var i = 0; i < data.posts.length; i++) {
                var post = data.posts[i];
                var new_post = $(post.html);
                list.prepend(new_post);
                getComments(post.id);
            }
        });
}

$(document).ready(function() {
    console.log("In ready");
    $("#post-btn").click(addPost);
    $("#post-field").keypress(function(e) {if (e.which == 13) addPost();});
    $("#post-list").on("click", "button", addComment);

    populateList();
    $("#post-field").focus();

    window.setInterval(getUpdates, 10000);

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