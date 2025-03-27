$(document).ready(function () {
    $('.btn.like').click((e) => {
        $.ajax({
            url: like_url,
            method: 'get',
            data: ,
            success: res => {
                if (res.is_auth) {
                    $(e.currentTarget).find('.bi.bi-heart, .bi.bi-heart-fill').addClass(res['add']).removeClass(res['remove'])
                    $(e.currentTarget).find('span').html(res['count'])
                } else {
                    alert("Доступно для авторизованных")
                }

            }
        });

    })
})