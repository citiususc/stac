$(document).on('ready', function() {

    //Visualización de selector de tipo y test POST-HOC si se requiere test no paramétrico de ranking.
    $("#test").change(function () {
        if($("#test").val()=="wilcoxon"){
            $("#mostrar_tipo").hide();
            $("#mostrar_comparacion").hide();
        }
        else{
            $("#mostrar_tipo").show();
            $("#mostrar_comparacion").show();
        }
    })
    .change();

    //Ejecución de los tests.
    $(document).on('click', '#datos', function() {

        var test = $('#test').val();
        var alpha = $('#alpha').val();
        var tipo = $('#tipo').val();
        var id_fichero = $('#seleccionar_hashmd5').val();
        var test_post_hoc = $("#test_post_hoc").val();

        if(id_fichero == "")
            alert("Falta HASH fichero")
        else{

            var url;
            if(alpha != "no" & tipo !="no")
                url = "http://localhost:8080/"+test+"/"+id_fichero+"/"+alpha+"/"+tipo;
            else if(alpha != "no")
                url = "http://localhost:8080/"+test+"/"+id_fichero+"/"+alpha;
            else if(tipo != "no")
                url = "http://localhost:8080/"+test+"/"+id_fichero+"/"+tipo;
            else
                url = "http://localhost:8080/"+test+"/"+id_fichero;

            var salida;

            $.ajax({
                type: "GET",
                url: url,
                dataType: "json",
                success : function(data) {
                    salida = "<u>Resultado test: "+test+"</u>";
                    $.each(data, function(key, val) {
                        salida = salida + "<p>" + key + " = " + val + "</p>";
                    });
                    "--------------"
                    if(data.resultado == "True" && test_post_hoc != "no"){

                        var url2;
                        if(alpha != "no")
                            url2 = "http://localhost:8080/"+test_post_hoc+"/"+test+"/"+data.nombres+"/"+data.ranking+"/"+data.N+"/"+alpha;
                        else
                            url2 = "http://localhost:8080/"+test_post_hoc+"/"+test+"/"+data.nombres+"/"+data.ranking+"/"+data.N;

                        $.ajax({
                            type: "GET",
                            url: url2,
                            dataType: "json",
                            success : function(data) {
                                salida = salida + "<p>---------------------------</p>"
                                salida = salida + "<u>Resultado POST-HOC "+test_post_hoc+":</u>";
                                $.each(data, function(key, val) {
                                    salida = salida + "<p>" + key + " = " + val + "</p>";
                                });
                                $("#resultado").html(salida);
                            },
                            error : function(e) {
                                alert('Error: ' + e);
                            }
                        });
                    }
                    "--------------"
                    $("#resultado").html(salida);
                },
                error : function(e) {
                    alert('Error: ' + e);
                }
            });
        }
    });

    //Subida de ficheros.
    $(document).on('click', '#boton_fichero', function() {

        var formData = new FormData($('#formfichero')[0]);
        var fichero = $("#fichero").val();

        if(!fichero)
            alert("Selecciona un fichero");
        else{
            $.ajax({
                type: "POST",
                url: "http://localhost:8080/fichero",
                dataType: "json",
                data: formData,
                cache: false,
                contentType: false,
                processData: false,
                success : function(data) {
                    resultado = "<p>Hash MD5 del fichero:</p>";
                    if(!data.fallo)
                        resultado = resultado + "<p>" + data.clave + "</p>";
                    else
                        resultado = resultado + "<p>" + data.fallo + "</p>";
                    $('#hash_fichero').html(resultado);
                    $('#formfichero').trigger('reset');
                },
                error : function(e) {
                    alert('Error: ' + e);
                }
            });
        }
    });

    //Consulta de ficheros.
    $(document).on('click', '#boton_consulta', function() {

        if( $("#consultar_hashmd5").val()!="") {
            var consulta_id = $('#consultar_hashmd5').val();
            console.log(consulta_id);
            $.ajax({
                type: "GET",
                url: "http://localhost:8080/fichero/"+consulta_id,
                success : function(data) {
                    salida = "<p>Contenido del fichero:</p>";
                    $.each(data, function(key, val) {
                        salida = salida + "<p>" + key + " = " + val + "</p>";
                    });
                    $('#contenido_fichero').html(salida);
                    $('#consultar_hashmd5').val("");
                },
                error : function(e) {
                    alert('Error: ' + e);
                }
            });
        }
        else{
            alert("Introduce hash del fichero");
        }
    });

});
