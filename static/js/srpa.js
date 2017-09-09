$(function(){
    $(document).on('click', 'img.captcha', function(){
        $.getJSON('/user/captcha/refresh', {}, function(json) {
            var img = $('#id_captcha_2');
            var hidden = $('#id_captcha_0');
            hidden.prop('value', json.key);
            img.prop('src', json.image_url);
        });
    });
});
