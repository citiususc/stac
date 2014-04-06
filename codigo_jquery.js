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

    //Función que redondea los datos devueltos por los tests.
    var redondear_valor = function(valor){
        if($.isArray(valor)){
            $.each(valor, function(indice,elemento){
                elementoFloat = parseFloat(elemento);
                if($.isNumeric(elementoFloat))
                    valor[indice] = elementoFloat.toFixed(3);
            });
        }
        else{
            if($.isNumeric(valor))
                valor = valor.toFixed(3);
        }
        return valor;
    };

    //Ejecución de los tests para comprobar los criterios paramétricos de normalidad y homocedasticidad.
    $(document).on('click', '#datos_criterios', function() {

        var test = $('#test_criterios').val();
        var id_fichero = $('#hashmd5_criterios').val();
        var alpha = $('#alpha_criterios').val();

        if(id_fichero == "")
            alert("Falta HASH fichero")
        else{

            var url;
            if(alpha != "no")
                url = "http://localhost:8080/"+test+"/"+id_fichero+"/"+alpha;
            else
                url = "http://localhost:8080/"+test+"/"+id_fichero;

            var salida;

            $.ajax({
                type: "GET",
                url: url,
                dataType: "json",
                success : function(data) {
                    salida = "<u>Resultado test criterio paramétrico:</u>";
                    if(data.fallo){
                        salida = salida + "<p>" + data.fallo + "</p>";
                    }
                    else{
                        $.each(data, function(key, val) {
                            salida = salida + "<p>" + key + " = " + redondear_valor(val) + "</p>";
                        });
                    }
                    $("#resultado_criterios").html(salida);
                },
                error : function(e) {
                    alert('Error: ' + e);
                }
            });
        }
    });

    //Ejecución de los tests paramétricos.
    $(document).on('click', '#datos_parametricos', function() {

        var test = $('#test_parametricos').val();
        var alpha = $('#alpha_parametricos').val();
        var id_fichero = $('#hashmd5_parametricos').val();

        if(id_fichero == "")
            alert("Falta HASH fichero")
        else{

            var url;
            if(alpha != "no")
                url = "http://localhost:8080/"+test+"/"+id_fichero+"/"+alpha;
            else
                url = "http://localhost:8080/"+test+"/"+id_fichero;

            var salida;

            $.ajax({
                type: "GET",
                url: url,
                dataType: "json",
                success : function(data) {
                    if(test == "ttest"){
                        salida = "<u>Resultado T-Test:</u>";
                        if(data.fallo){
                            salida = salida + "<p>" + data.fallo + "</p>";
                        }
                        else{
                            $.each(data, function(key, val) {
                                salida = salida + "<p>" + key + " = " + redondear_valor(val) + "</p>";
                            });
                        }
                    }
                    else{
                        salida = "<u>Resultado test ANOVA:</u>";
                        if(data.fallo){
                            salida = salida + "<p>" + data.fallo + "</p>";
                        }
                        else{
                            $.each(data.test_anova, function(key, val) {
                                salida = salida + "<p>" + key + " = " + redondear_valor(val) + "</p>";
                            });
                            salida = salida + "<u>Resultado test POST-HOC Bonferroni:</u>";
                            if(!data.test_comparacion){
                                salida = salida + "<p>El test de ranking no es estadísticamente significativo</p>";
                            }
                            else{
                                $.each(data.test_comparacion, function(key, val) {
                                    salida = salida + "<p>" + key + " = " + redondear_valor(val) + "</p>";
                                });
                            }
                        }
                    }
                    $("#resultado_parametricos").html(salida);
                },
                error : function(e) {
                    alert('Error: ' + e);
                }
            });
        }
    });

    //Ejecución de los tests no paramétricos.
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
            if(alpha != "no" && tipo != "no" && test_post_hoc != "no")
                url = "http://localhost:8080/"+test+"/"+id_fichero+"/"+alpha+"/"+tipo+"/"+test_post_hoc;
            else if(test_post_hoc != "no" && alpha != "no")
                url = "http://localhost:8080/"+test+"/"+id_fichero+"/"+alpha+"/"+test_post_hoc;
            else if(test_post_hoc != "no" && tipo != "no")
                url = "http://localhost:8080/"+test+"/"+id_fichero+"/"+tipo+"/"+test_post_hoc;
            else if(test_post_hoc != "no")
                url = "http://localhost:8080/"+test+"/"+id_fichero+"/"+test_post_hoc;
            else if(alpha != "no" & tipo !="no")
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
                    if(test == "wilcoxon"){
                        salida = "<u>Resultado test Wilcoxon:</u>";
                        if(data.fallo){
                            salida = salida + "<p>" + data.fallo + "</p>";
                        }
                        else{
                            $.each(data, function(key, val) {
                                salida = salida + "<p>" + key + " = " + redondear_valor(val) + "</p>";
                            });
                        }
                    }
                    else{
                        salida = "<u>Resultado test Ranking:</u>";
                        if(data.fallo){
                            salida = salida + "<p>" + data.fallo + "</p>";
                        }
                        else{
                            $.each(data.test_ranking, function(key, val) {
                                salida = salida + "<p>" + key + " = " + redondear_valor(val) + "</p>";
                            });
                            salida = salida + "<u>Resultado test Comparación:</u>";
                            if(!data.test_comparacion){
                                salida = salida + "<p>El test de ranking no es estadísticamente significativo</p>";
                            }
                            else{
                                $.each(data.test_comparacion, function(key, val) {
                                    salida = salida + "<p>" + key + " = " + redondear_valor(val) + "</p>";
                                });
                            }
                        }
                    }
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
                    resultado = "<u>Resumen HASH del fichero:</u>";
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
                    salida = "<u>Contenido del fichero:</u>";
                    if(data.fallo){
                        salida = salida + "<p>" + data.fallo + "</p>";
                    }
                    else{
                        $.each(data, function(key, val) {
                            salida = salida + "<p>" + key + " = " + val + "</p>";
                        });
                    }
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
