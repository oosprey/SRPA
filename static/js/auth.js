function form_callback(data){
    var form = $('#form');
    form.fadeOut(0);
    $('#form').html(data);
    form.fadeIn(500);
}

function load_auth_form(type)
{
    $.ajax({
        url: '/accounts/load_auth_form',
        type: 'GET', 
        data: {'form_type': type},
        success: form_callback,
    });
}
