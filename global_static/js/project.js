$(function () {
    $('.srpa-loader[loader-type="page"]').first().click();
    var x = 0;
    $("#add-one-term").click(function(){
        x = x + 1;
        var div = document.createElement('div');
        div.className = "form-group budget";
        div.dataset.toggle = "tooltip";
        div.dataset.placement="top";
        div.title="请按照格式填写";
        var div2 = document.createElement('div');
        div2.className = "col-sm-2";
        var label = document.createElement('label');
        label.className = "control-label";
        label.innerHTML = '预算明细'+x+':';
        div2.appendChild(label);
        var div3 = document.createElement('div');
        div3.className = "col-sm-10";
        var input1 = document.createElement('input');
        input1.className = "col-sm-4";
        input1.name = "item_"+x;
        input1.placeholder = "预算项目";
        input1.type = "text";
        input1.style = "color:#000000;";
        var input2 = document.createElement('input');
        input2.className = "col-sm-4";
        input2.placeholder = "预算金额";
        input2.type = "number";
        input2.name = "amount_"+x;
        input2.style = "color:#000000;";
        var input3 = document.createElement('input');
        input3.className = "col-sm-4";
        input3.placeholder = "预算描述";
        input3.name = "detail_"+x;
        input3.type = "text";
        input3.style = "color:#000000;";
        div3.appendChild(input1);
        div3.appendChild(input2);
        div3.appendChild(input3);
        div.appendChild(div2);
        div.appendChild(div3);
        var form = document.getElementById("data-forms");
        form.appendChild(div);
    });
})
function clean_js()
{
    $('.form_datetime_hour').datetimepicker('remove');
}
function init_js()
{
    $('[data-toggle="tooltip"]').tooltip();
    $('.form_datetime_hour').datetimepicker({
        format: 'yyyy-mm-dd hh:00:00',
        weekStart: 1,
        autoclose: true,
        todayBtn: true,
        minView: 1,
    });
    $('#info-form').on('submit', function(e){
        var form = $('#info-form');
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: form.attr('action'),
            data: form.serialize(),
            success: function(data){
                if(data.status == 0)
                    window.location.href=data.redirect;
                else
                {
                    if(data.status != 1)
                        alert(data.reason);
                    $('#status_table').html('');
                }
                clean_js();
                $('#page').html(data.html);
                init_js();
            },
            error: function(request, data){
                alert('与服务器通信发生错误');
            }
        });
    });
    $('#upfile-form').on('submit', function(e){
        var formData = new FormData();
        var form = $('#upfile-form');
        e.preventDefault();
        formData.append("attachment",$("#id_attachment")[0].files[0]);
        $.ajax({ 
            url : form.attr('action'), 
            type : 'POST', 
            data : formData, 
            processData : false, 
            contentType : false,
            success: function(data){
               if(data.status == 0)
                    window.location.href=data.redirect;
                else
                {
                    if(data.status != 1)
                        alert(data.reason);
                    $('#status_table').html('');
                }
                clean_js();
                $('#page').html(data.html);
                init_js();
            },
            error: function(request, data){
                alert('与服务器通信发生错误');
            }
        });
    });
}