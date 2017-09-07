$(function(){
    $("#add-one-term").click(function(){
        $('div.data-row:last').clone().each(function(i) {
            $(this).find('input,select').each(function(i) {

                // Remove any existing values 
                $(this).val('');

                // update the id attributes, incrementing the form number, e.g.: "id_form-1-field_name"
                parts = $(this).attr('id').split('-', 3); 
                num = parseInt(parts[1]) + 1;
                $(this).attr('id', parts[0] + '-' +num + '-' +parts[2]);

                // Update the name attribute, e.g.: form-1-field_name
                parts = $(this).attr('name').split('-', 3); 
                num = parseInt(parts[1]) + 1; 
                $(this).attr('name', parts[0] + '-' +num + '-' +parts[2]);

            }); 

            // Update the "for" attribute for all labels 
            $(this).find('label').each(function(i) {
                parts = $(this).attr('for').split('-', 3); 
                num = parseInt(parts[1]) + 1;
                $(this).attr('for', parts[0] + '-' +num + '-' +parts[2]);
            }); 

        }).appendTo('div#data-forms');
        $("#id_form-TOTAL_FORMS").val(parseInt($('#id_form-TOTAL_FORMS').val())+1);
    });
    $(".delete-sheet").click(function(){
        if(!confirm('确认要删除该报销单吗?'))
            return;
        var uid = $(this).attr('sheet-uid');
        var form = $("#billsheet_list_form");
        var url = form.attr('action');
        $.ajax({
            method: 'POST',
            url: url + uid,
            data: form.serialize(),
            success: function(data){window.location.reload();}
        });
    });
});
function delete_bill_info(uid)
{
    $.ajax({
        method: 'get',
        url: '/bills/bill_info/delete/' + uid,
        success: function(data){
            if(data.status == 0)
            {
                if(confirm(data.msg))
                    window.location.href = data.redirect;
                else
                    window.location.reload();
            }
            else if(data.status == 1)
            {
                alert(data.msg);
                window.location.href = data.redirect;
            }
            else
                alert(data.msg);
        }
    });
}
