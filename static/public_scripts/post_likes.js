(function($){
    $('.like-form').click(function(ev){
        ev.preventDefault();

        var csrfToken = $("input[name=csrfmiddlewaretoken]").val();
        const post_id = $(this).attr('id');
        const dataUrl = $(this).attr('action')

        const likesValue = $(`.likes-btn${post_id}`).text()
        const likesValueTrim = likesValue.trim()

        const likeCount = $(`.likes-count${post_id}`).text()
        const likesCountTrim = parseInt(likeCount)
        let res;

        $.ajax({
            type: 'POST',
            dataType: 'json',
            url: dataUrl,
            data: {
                'csrfmiddlewaretoken': csrfToken,
                'like_id': post_id //like_id the name on my form
            },
            success: function(response){
                if (likesValueTrim === 'Unlike'){
                        $(`.likes-btn${post_id}`).text('Like')
                        res = likesCountTrim - 1
                    }else{
                        $(`.likes-btn${post_id}`).text('Unlike')
                        res = likesCountTrim + 1
                    }
                    let spacebar = $("<span>&nbsp;</span>").text()
                    $(`.likes-count${post_id}`).text(res).append(spacebar).append('likes')
            },
        
            error: function(response){
                console.log('error', response)
            }
        })
    })
})(jQuery);