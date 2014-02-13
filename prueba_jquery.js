$(document).on('ready', function() {

    $(document).on('click', '#datos', function() {

        var test = $('#test').val();
        var alpha = $('#alpha').val();
        var tipo = $('#tipo').val();

        var url = "http://localhost:8080/"+test+"/"+alpha+"/"+tipo;

        $.ajax({
            type: "get",
            url: url,
            dataType: "json",
            success : function(data) {
                salida = "<p>Salida:</p>";
                $.each(data, function(key, val) {
                    salida = salida + "<p>" + key + " = " + val + "</p>";
                });
                $("#resultado").html(salida);
            },
            error : function(e) {
                alert('Error: ' + e);
            }
        });

    })

});