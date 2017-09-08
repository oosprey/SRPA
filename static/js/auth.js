function load_auth_form(type)
{
    $.ajax({
        url: '/accounts/load_auth_form',
        type: 'GET', 
        data: {'form_type': type},
        success: load_form_callback,
    });
}
function load_form_callback(data)
{
    $('#register_form').html(data);
}
