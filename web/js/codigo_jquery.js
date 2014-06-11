$(document).on('ready', function() {

	//Para obtener la url base. Compatible con los navegadores: Chrome 27, Firefox 23, Safari 6, Internet Explorer 10.
	if (!window.location.origin)
 		window.location.origin = window.location.protocol+"//"+window.location.host;

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
        var alpha = $('#alpha_criterios').val();

        if(localStorage.getItem("fichero_actual") == null)
            alert("Sube un fichero")
        else{

            var url;
            if(alpha != "no")
                url = window.location.origin+"/stac/beta/api/"+test+"/"+localStorage.getItem("fichero_actual")+"/"+alpha;
            else
                url = window.location.origin+"/stac/beta/api/"+test+"/"+localStorage.getItem("fichero_actual");

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

        if(localStorage.getItem("fichero_actual") == null)
            alert("Sube un fichero")
        else{

            var url;
            if(alpha != "no")
                url = window.location.origin+"/stac/beta/api/"+test+"/"+localStorage.getItem("fichero_actual")+"/"+alpha;
            else
                url = window.location.origin+"/stac/beta/api/"+test+"/"+localStorage.getItem("fichero_actual");

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
        var test_post_hoc = $("#test_post_hoc").val();

        if(localStorage.getItem("fichero_actual") == "")
            alert("Falta fichero")
        else{

            var url;
            if(alpha != "no" && tipo != "no" && test_post_hoc != "no")
                url = window.location.origin+"/stac/beta/api/"+test+"/"+localStorage.getItem("fichero_actual")+"/"+alpha+"/"+tipo+"/"+test_post_hoc;
            else if(test_post_hoc != "no" && alpha != "no")
                url = window.location.origin+"/stac/beta/api/"+test+"/"+localStorage.getItem("fichero_actual")+"/"+alpha+"/"+test_post_hoc;
            else if(test_post_hoc != "no" && tipo != "no")
                url = window.location.origin+"/stac/beta/api/"+test+"/"+localStorage.getItem("fichero_actual")+"/"+tipo+"/"+test_post_hoc;
            else if(test_post_hoc != "no")
                url = window.location.origin+"/stac/beta/api/"+test+"/"+localStorage.getItem("fichero_actual")+"/"+test_post_hoc;
            else if(alpha != "no" & tipo !="no")
                url = window.location.origin+"/stac/beta/api/"+test+"/"+localStorage.getItem("fichero_actual")+"/"+alpha+"/"+tipo;
            else if(alpha != "no")
                url = window.location.origin+"/stac/beta/api/"+test+"/"+localStorage.getItem("fichero_actual")+"/"+alpha;
            else if(tipo != "no")
                url = window.location.origin+"/stac/beta/api/"+test+"/"+localStorage.getItem("fichero_actual")+"/"+tipo;
            else
                url = window.location.origin+"/stac/beta/api/"+test+"/"+localStorage.getItem("fichero_actual");

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
                url: window.location.origin+"/stac/beta/api/fichero",
                dataType: "json",
                data: formData,
                cache: false,
                contentType: false,
                processData: false,
                success : function(data) {
                    resultado = "";
                    if(!data.fallo){
                        resultado = "<p>Fichero subido con éxito</p>";
						localStorage.setItem("fichero_actual", data.clave);
					}
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

});
