$(function () {
    init_js();
    $('.page-loader').on('click', function(e){
        var load_target = $(this).attr('load-target');
        var target = this;
        if($(target).parent().hasClass('active'))
            return;
        $.ajax({
            type: 'GET',
            url: load_target,
            success: function(data){
                clean_js();
                $("#reservation_content").html(data);
                $('li.active').removeClass('active');
                $(target).parent().addClass('active');
                init_js();
            }
        });
    });
    $('.page-loader').first().click();
})
function clean_js()
{
    $('#dt_div').datetimepicker('remove');
}
function init_js()
{
    $('[data-toggle="tooltip"]').tooltip();
    $("#dt_div").datetimepicker({
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
}
