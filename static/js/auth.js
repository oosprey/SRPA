function project_callback(data){
    var project_item = $('#project_item');
    project_item.fadeOut(0);
    $('#project_item').html(data);
    project_item.fadeIn(500);
}
