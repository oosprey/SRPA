$('.datetimepicker').datetimepicker({
    format: 'yyyy-mm-dd hh:mm',
    autoclose: true,
});
$(function(){
    $('#search-form').submit(function(e){
        e.preventDefault();
        var form = $('#search-form');
        $.ajax({
            method: 'POST',
            url: form.attr('action'),
            data: form.serialize(),
            success: function(data){
                $('#statistic_table').html(data);
            },
        });
    });
});
