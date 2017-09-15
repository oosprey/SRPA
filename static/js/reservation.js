$(function () {
    $(".form_datetime").datetimepicker({
        format: "yyyy/mm/dd",
        weekStart: 1,
        autoclose: true,
        todayBtn: true,
        startDate: "{% now 'Y/m/d' %}",
        minView: 2,
    });
    $('[data-toggle="tooltip"]').tooltip();
    $('#search-form').on('submit', function(e){
        e.preventDefault();
        $.ajax({
            type: 'POST',
            data: $('#search-form').serialize(),
            success: function(data){
                if(data.status == 1)
                    alert('请选择有效时间');
                else if(data.status == 0)
                    $('#status_table').html(data.html);
            },
        });
    });
})
