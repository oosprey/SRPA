function load_register_form(type)
{
    $.ajax({
        url: '/accounts/load_register_form',
        type: 'GET', 
        data: {'register_type': type},
        success: load_form_callback,
    });
}
function load_form_callback(data)
{
    $('#register_form').html(data);
}
