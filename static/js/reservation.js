$(function () {
    re_init_js();
})
function re_init_js()
{
    $('[data-toggle="tooltip"]').tooltip();
    $(".form_datetime").datetimepicker({
        format: "yyyy/mm/dd",
        weekStart: 1,
        autoclose: true,
        todayBtn: true,
        minView: 2,
    });
    $('#search-form').on('submit', function(e){
        var form = $('#search-form');
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: form.attr('action'),
            data: form.serialize(),
            success: function(data){
                if(data.status == 0)
                    $('#status_table').html(data.html);
                else
                {
                    alert(data.reason);
                    $('#status_table').html('');
                }
            },
        });
    });
    $('.page-loader').on('click', function(e){
        alert($(this).attr('load-target'));
    });
}
