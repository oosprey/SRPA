$('.captcha').click(function(){
    $.getJSON('/captcha/refresh', {}, function(json) {
        var img = $('#id_captcha_2');
        var hidden = $('#id_captcha_0');
        hidden.prop('value', json.key);
        img.prop('src', json.img);
    });
    return false;
});
