$('document').ready(function(){
    $('#form').submit(function (event) {
        event.preventDefault();
        var id_code = $('#id_code').val();
        alert(id_code);
        $.ajax({
            type : 'POST',
            url : 'http://hearts3.herokuapp.com/find',
            data : {id: id_code},
            success : function(data){
                alert(data);
            }
        });
    });
});