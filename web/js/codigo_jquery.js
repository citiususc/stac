$(document).on('ready', function() {

	//Para obtener la url base. Compatible con los navegadores: Chrome 27, Firefox 23, Safari 6, Internet Explorer 10.
	if (!window.location.origin)
 		window.location.origin = window.location.protocol+"//"+window.location.host;

    //Ejecución del test de Levene para comprobar el criterio de homocedasticidad.
    $(document).on('click', '#datos_homocedasticidad', function() {

        var alpha = $('#alpha_homocedasticidad').val();

        if(localStorage.getItem("fichero_actual") == null)
            $("#alerta_fichero_homocedasticidad").show();
        else{

            var url;
            if(alpha != "no")
                url = window.location.origin+"/stac/beta/api/levene/"+localStorage.getItem("fichero_actual")+"/"+alpha;
            else
                url = window.location.origin+"/stac/beta/api/levene/"+localStorage.getItem("fichero_actual");

            var salida;

            $.ajax({
                type: "GET",
                url: url,
                dataType: "json",
                success : function(data) {
                    salida = "<br><u>Resultado test de homocedasticidad de Levene:</u>";

                    $("#alerta_fichero_homocedasticidad").hide();

                    if(data.fallo){
                        $("#alerta_fichero_homocedasticidad").show();
                    }
                    else{
                        salida = salida + generar_tabla_levene(data);
                        if(data.resultado==false)
                            localStorage.setItem("homocedasticidad", "cumple");
                        else
                            localStorage.setItem("homocedasticidad", "no_cumple");
                    }
                    $("#resultado_homocedasticidad").html(salida);
                },
                error : function(e) {
                    alert('Error: ' + e);
                }
            });
        }
    });

    //Ejecución de los tests para comprobar los criterios paramétricos de normalidad.
    $(document).on('click', '#datos_normalidad', function() {

        var test = $('input[name=test]:checked').val();
        var alpha = $('#alpha_normalidad').val();

        if(localStorage.getItem("fichero_actual") == null)
            $("#alerta_fichero").show();
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
                    salida = "<br><u>Resultado test criterio paramétrico:</u>";

                    $("#alerta_fichero").hide();

                    if(data.fallo){
                        $("#alerta_fichero").show();
                    }
                    else{
                        salida = salida + generar_tabla_normalidad(data,test);
                        var i;
                        var cumple = 1;
                        for(i=0;i<data.resultado.length;i++){
                            if(data.resultado[i] == true)
                                cumple = 0;
                        }
                        if(cumple == 0)
                            localStorage.setItem("normalidad", "no_cumple");
                        else
                            localStorage.setItem("normalidad", "cumple");
                    }
                    $("#resultado").html(salida);
                },
                error : function(e) {
                    alert('Error: ' + e);
                }
            });
        }
    });

    //Ejecución del test paramétrico Anova.
    $(document).on('click', '#datos_anova', function() {

        var alpha = $('#alpha_anova').val();

        if(localStorage.getItem("fichero_actual") == null)
            $("#alerta_fichero").show();
        else if(localStorage.getItem("homocedasticidad") == "no" && localStorage.getItem("normalidad") == "no")
            $("#fallo_test").html("Realiza los tests de condiciones paramétricas para determinar si se pueden aplicar los tests paramétricos.").show();
        else if(localStorage.getItem("homocedasticidad") == "no")
            $("#fallo_test").html("Realiza el test de Levene en \"Condiciones paramétricas\" para determinar si los datos cumplen con la característica de homocedasticidad.").show();
        else if(localStorage.getItem("normalidad") == "no")
            $("#fallo_test").html("Realiza algún test de normalidad en \"Condiciones paramétricas\" para determinar si los datos cumplen con la característica de normalidad.").show();
        else if(localStorage.getItem("homocedasticidad") == "no_cumple" || localStorage.getItem("normalidad") == "no_cumple")
            $("#fallo_test").html("No se pueden aplicar los tests paramétricos, ya que no cumplen las condiciones paramétricas. Prueba a realizar de nuevo los tests de condiciones paramétricas con distintos niveles de confianza.").show();
        else{

            var url;
            if(alpha != "no")
                url = window.location.origin+"/stac/beta/api/anova/"+localStorage.getItem("fichero_actual")+"/"+alpha;
            else
                url = window.location.origin+"/stac/beta/api/anova/"+localStorage.getItem("fichero_actual");

            var salida;

            $.ajax({
                type: "GET",
                url: url,
                dataType: "json",
                success : function(data) {
                    salida = "<br><u>Resultado test ANOVA:</u>";
                
                    $("#fallo_test").hide();
                    $("#alerta_fichero").hide();
    
                    if(data.fallo){
                        $("#alerta_fichero").show();
                    }
                    else{
                        salida = salida + generar_tabla_parametricos(data.test_anova,"anova");
                        salida = salida + "<br><u>Resultado test POST-HOC Bonferroni:</u>";
                        if(!data.test_comparacion){
                            salida = salida + "<p>El test de ranking no es estadísticamente significativo</p>";
                        }
                        else{
                            salida = salida + generar_tabla_multitests(data.test_comparacion,"bonferroni");
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

    //Ejecución del test paramétrico T-test.
    $(document).on('click', '#datos_ttest', function() {

        var alpha = $('#alpha_ttest').val();

        if(localStorage.getItem("fichero_actual") == null)
            $("#alerta_fichero_ttest").show();
        else if(localStorage.getItem("homocedasticidad") == "no" && localStorage.getItem("normalidad") == "no")
            $("#fallo_test_ttest").html("Realiza los tests de condiciones paramétricas para determinar si se pueden aplicar los tests paramétricos.").show();
        else if(localStorage.getItem("homocedasticidad") == "no")
            $("#fallo_test_ttest").html("Realiza el test de Levene en \"Condiciones paramétricas\" para determinar si los datos cumplen con la característica de homocedasticidad.").show();
        else if(localStorage.getItem("normalidad") == "no")
            $("#fallo_test_ttest").html("Realiza algún test de normalidad en \"Condiciones paramétricas\" para determinar si los datos cumplen con la característica de normalidad.").show();
        else if(localStorage.getItem("homocedasticidad") == "no_cumple" || localStorage.getItem("normalidad") == "no_cumple")
            $("#fallo_test_ttest").html("No se pueden aplicar los tests paramétricos, ya que no cumplen las condiciones paramétricas. Prueba a realizar de nuevo los tests de condiciones paramétricas con distintos niveles de confianza.").show();
        else{

            var url;
            if(alpha != "no")
                url = window.location.origin+"/stac/beta/api/ttest/"+localStorage.getItem("fichero_actual")+"/"+alpha;
            else
                url = window.location.origin+"/stac/beta/api/ttest/"+localStorage.getItem("fichero_actual");

            var salida;

            $.ajax({
                type: "GET",
                url: url,
                dataType: "json",
                success : function(data) {
                    salida = "<br><u>Resultado T-test:</u>";
                
                    $("#fallo_test_ttest").hide();
                    $("#alerta_fichero_ttest").hide();
    
                    if(data.fallo){
                        if(data.fallo.indexOf("fichero") > -1)
                            $("#alerta_fichero_ttest").show();
                        else
                            $("#fallo_test_ttest").html(data.fallo).show();
                    }
                    else{
                        salida = salida + generar_tabla_parametricos(data,"ttest");
                    }
                    $("#resultado_ttest").html(salida);
                },
                error : function(e) {
                    alert('Error: ' + e);
                }
            });
        }
    });

    //Ejecución del test de Wilcoxon.
    $(document).on('click', '#datos_wilcoxon', function() {

        var alpha = $('#alpha').val();
        
        if(localStorage.getItem("fichero_actual") == null)
            $("#alerta_fichero").show();
        else{
            
            var url;
            
            if(alpha != "no")
                url = window.location.origin+"/stac/beta/api/wilcoxon/"+localStorage.getItem("fichero_actual")+"/"+alpha;
            else
                url = window.location.origin+"/stac/beta/api/wilcoxon/"+localStorage.getItem("fichero_actual");

            var salida = "";
        
            $.ajax({
                type: "GET",
                url: url,
                dataType: "json",

                success : function(data) {
                    salida = "<br><u>Resultado test Wilcoxon:</u>";
                
                    $("#fallo_test").hide();
                    $("#alerta_fichero").hide();

                    if(data.fallo){
                        if(data.fallo.indexOf("fichero") > -1)
                            $("#alerta_fichero").show();
                        else
                            $("#fallo_test").html(data.fallo).show();
                    }
                    else{
                        salida = salida + generar_tabla_wilcoxon(data);
                    }
                    $("#resultado").html(salida);
                },
                error : function(e) {
                    alert('Error: ' + e);
                }
            });
        }
    });

    //Ejecución de los tests no paramétricos de ranking.
    $(document).on('click', '#datos_ranking', function() {

        var test = $('input[name=test]:checked').val();
        var alpha = $('#alpha').val();
        var tipo = $('#tipo').val();
        var test_post_hoc = $('input[name=post_hoc]:checked').val();
        
        if(test_post_hoc === undefined)
            test_post_hoc = "no";

        if(localStorage.getItem("fichero_actual") == null)
            $("#alerta_fichero_ranking").show();
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

            var salida = "";
        
            $.ajax({
                type: "GET",
                url: url,
                dataType: "json",

                success : function(data) {
                    salida = salida + "<br><u>Resultado test Ranking:</u>";

                    $("#alerta_fichero_ranking").hide();

                    if(data.fallo){
                        $("#alerta_fichero_ranking").show();
                    }
                    else{
                        salida = salida + generar_tabla_ranking(data.test_ranking)
                        salida = salida + "<br><u>Resultado test Post-Hoc:</u>";
                        if(!data.test_comparacion){
                            salida = salida + "<p>El test de ranking no es estadísticamente significativo.</p>";
                        }
                        else{
                            if(test_post_hoc.indexOf("multi") > -1)
                                salida = salida + generar_tabla_multitests(data.test_comparacion,test_post_hoc);
                            else
                                salida = salida + generar_tabla_control(data.test_comparacion,test_post_hoc);
                        }
                    }
                    $("#resultado_ranking").html(salida);
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
            $('#mensaje_subida').html("<br><p style=\"color:red\";><strong>Selecciona un fichero</strong></p>");
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
                        resultado = "<p style=\"color:green\";><strong>Fichero subido con éxito</strong></p>";
						localStorage.setItem("fichero_actual", data.clave);
                        localStorage.setItem("homocedasticidad", "no");
                        localStorage.setItem("normalidad", "no");
					}
                    else
                        resultado = resultado + "<p style=\"color:red\";><strong>" + data.fallo + "</strong></p>";
                    $('#mensaje_subida').html("<br>"+resultado);
                    $('#formfichero').trigger('reset');
                },
                error : function(e) {
                    alert('Error: ' + e);
                }
            });
        }
    });

    //Para limpiar el mensaje previo de subida de fichero.
    $(document).on('click', '#a_subida', function() {
        $('#mensaje_subida').html("");
    });

    //Gestión botón de subida de ficheros.
    $(document).on('change', '.btn-file :file', function() {
      var input = $(this),
          numFiles = input.get(0).files ? input.get(0).files.length : 1,
          label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
      input.trigger('fileselect', [numFiles, label]);
    });

    $('.btn-file :file').on('fileselect', function(event, numFiles, label) {
        
        var input = $(this).parents('.input-group').find(':text'),
            log = numFiles > 1 ? numFiles + ' files selected' : label;
        
        if( input.length ) {
            input.val(log);
        } else {
            if( log ) alert(log);
        }
        
    });
});


//Función javascript para generar la tabla de resultados para los tests paramétricos de Anova y T-test.
function generar_tabla_parametricos(data,test) {

    var salida = "<div class=\"table-responsive\"><br><table class=\"table table-hover\"><tbody>";
    if(test == "anova")
        salida = salida + "<tr><th>Estadístico:</th><td>" +data.estadistico.toFixed(3)+ "</td></tr>";
    else
        salida = salida + "<tr><th>Estadístico T:</th><td>" +data.estadistico_t.toFixed(3)+ "</td></tr>";
    salida = salida + "<tr><th>p-valor:</th><td>" +data.p_valor.toFixed(3)+ "</td></tr>";
    if(data.resulado == true)
        salida = salida + "<tr><th>Resultado:</th><td>Se rechaza H0</td></tr>";
    else
        salida = salida + "<tr><th>Resultado:</th><td>Se acepta H0</td></tr>";
    salida = salida + "</tbody></table></div>";

    return salida;
}

//Función javascript para generar la tabla de resultados para el test de condición de homocedasticidad de Levene.
function generar_tabla_levene(data) {

    var salida = "<div class=\"table-responsive\"><br><table class=\"table table-hover\"><tbody>";
    salida = salida + "<tr><th>Estadístico W:</th><td>" +data.estadistico_w.toFixed(3)+ "</td></tr>";
    salida = salida + "<tr><th>p-valor:</th><td>" +data.p_valor.toFixed(3)+ "</td></tr>";
    if(data.resulado == true)
        salida = salida + "<tr><th>Resultado:</th><td>Se rechaza H0</td></tr>";
    else
        salida = salida + "<tr><th>Resultado:</th><td>Se acepta H0</td></tr>";
    salida = salida + "</tbody></table></div>";

    return salida;
}

//Función javascript para generar la tabla de resultados de los tests de condición de normalidad.
function generar_tabla_normalidad(data, test) {

    //Primera fila de la tabla.
    var salida = "<div class=\"table-responsive\"><br><table class=\"table table-hover\"><thead><tr><th></th>";
    
	$.each(data.p_valores, function(index, value) {
		salida = salida + "<th>Población " + (index+1) + "</th>";
	});

    //Resto de filas de la tabla.
    if(test == "shapiro"){
	    salida = salida + "</tr></thead><tbody><tr><th>Estadísticos W:</th>";
	    $.each(data.estadisticos_w, function(index, value) {
		    salida = salida + "<td>" + value.toFixed(3) + "</td>";
	    });
        salida = salida + "</tr>";
    }
    else if(test == "kolmogorov"){
	    salida = salida + "</tr></thead><tbody><th>Estadísticos D:</th>";
	    $.each(data.estadisticos_d, function(index, value) {
		    salida = salida + "<td>" + value.toFixed(3) + "</td>";
	    });
        salida = salida + "</tr>";
    }
    else{
	    salida = salida + "</tr></thead><tbody><th>Estadísticos K2:</th>";
	    $.each(data.estadisticos_k2, function(index, value) {
		    salida = salida + "<td>" + value.toFixed(3) + "</td>";
	    });
        salida = salida + "</tr>";
    }

    salida = salida + "<tr><th>p-valores:</th>";

	$.each(data.p_valores, function(index, value) {
		salida = salida + "<td>" + value.toFixed(3) + "</td>";
	});

    salida = salida + "</tr><tr><th>Resultados:</th>";

    $.each(data.resultado, function(index, value) {
		if(value == true)
            salida = salida + "<td>Se rechaza H0</td>";
        else
            salida = salida + "<td>Se acepta H0</td>";
	});

	salida = salida + "</tr></tbody></table></div>";

    return salida;
}

//Función javascript para generar la tabla de resultados del test de Wilcoxon.
function generar_tabla_wilcoxon(data) {

    var salida = "<div class=\"table-responsive\"><br><table class=\"table table-hover\"><tbody>";
    salida = salida + "<tr><th>Estadístico:</th><td>" +data.estadistico+ "</td></tr>";
    salida = salida + "<tr><th>Punto crítico:</th><td>" +data["punto critico"]+ "</td></tr>";
    salida = salida + "<tr><th>Suma de rangos positivos:</th><td>" +data["suma rangos pos"]+ "</td></tr>";
    salida = salida + "<tr><th>Suma de rangos negativos:</th><td>" +data["suma rangos neg"]+ "</td></tr>";
    if(data.resulado == true)
        salida = salida + "<tr><th>Resultado:</th><td>Se rechaza H0</td></tr>";
    else
        salida = salida + "<tr><th>Resultado:</th><td>Se acepta H0</td></tr>";
    salida = salida + "</tbody></table></div>";

    return salida;
}

//Función javascript para generar la tabla de resultados de los tests de ranking.
function generar_tabla_ranking(data) {

    var salida = "<div class=\"table-responsive\"><br><table class=\"table table-hover\"><tbody><tr><th>Ranking:</th>";
    
	$.each(data.ranking, function(index, value) {
		salida = salida + "<td>" + value.toFixed(3); + "</td>";
	});

    salida = salida + "</tr><th>Algoritmos:</th>";

	$.each(data.nombres, function(index, value) {
		salida = salida + "<td>" + value + "</td>";
	});

    salida = salida + "</tr><th>Estadístico:</th><td>" + data.estadistico.toFixed(3); + "</td></tr>";
    salida = salida + "</tr><th>p-valor:</th><td>" + data.p_valor.toFixed(3); + "</td></tr>";
    if(data.resultado == true)
        salida = salida + "</tr><th>Resultado:</th><td>Se rechaza H0</td></tr>";
    else
        salida = salida + "</tr><th>Resultado:</th><td>Se acepta H0</td></tr>";

    salida = salida + "</tbody></table></div>";

    return salida;
}

//Función javascript para generar la tabla de resultados de los tests Post-Hoc con método de control.
function generar_tabla_control(data, test) {

    var salida = "<div class=\"table-responsive\"><br><table class=\"table table-hover\"><tbody><tr><th>Método de Control:</th><td>" +data.metodo_control+ "</td></tr>";

    if(test != "li_test"){
        if(test == "no" || test == "bonferroni_dunn_test")
            salida = salida + "<tr><th>alpha Ajustado:</th><td>" + data.alpha.toFixed(3) + "</td></tr>";
        else{
            salida = salida + "</tr><tr><th>alphas ajustados:</th>";
            $.each(data.alphas, function(index, value) {
		        salida = salida + "<td>" + value.toFixed(3) + "</td>";
	        });
        }
    }
    
    salida = salida + "</tr><tr><th>Método control VS:</th>";

	$.each(data.nombres, function(index, value) {
		salida = salida + "<td>" + value + "</td>";
	});

    salida = salida + "</tr><tr><th>Estadísticos:</th>";

	$.each(data.valores_z, function(index, value) {
		salida = salida + "<td>" + value.toFixed(3) + "</td>";
	});

    salida = salida + "</tr><tr><th>p-valores:</th>";

	$.each(data.p_valores, function(index, value) {
		salida = salida + "<td>" + value.toFixed(3) + "</td>";
	});

    salida = salida + "</tr><tr><th>p-valores ajustados:</th>";

	$.each(data.p_valores_ajustados, function(index, value) {
		salida = salida + "<td>" + value.toFixed(3) + "</td>";
	});

    salida = salida + "</tr><tr><th>Resultados:</th>";

    $.each(data.resultado, function(index, value) {
		if(value == true)
            salida = salida + "<td>Se rechaza H0</td>";
        else
            salida = salida + "<td>Se acepta H0</td>";
	});

    salida = salida + "</tbody></table></div>";
    
    return salida;
}

//Función javascript para generar la tabla de resultados de los tests Post-Hoc multitests.
function generar_tabla_multitests(data, test) {

    var salida = "<div class=\"table-responsive\"><br><table class=\"table table-hover\"><tbody>";

    if(test == "nemenyi_multitest" || test == "bonferroni")
        salida = salida + "<tr><th>alpha ajustado:</th><td>" + data.alpha.toFixed(3) + "</td></tr>";
    else{
        salida = salida + "<tr><th>alphas ajustados:</th>";
        $.each(data.alphas, function(index, value) {
	        salida = salida + "<td>" + value.toFixed(3) + "</td>";
        });
        salida = salida + "</tr>";
    }

    salida = salida + "<tr><th>Comparaciones:</th>"
    
	$.each(data.comparaciones, function(index, value) {
		salida = salida + "<td>" + value + "</td>";
	});

    salida = salida + "</tr><th>Estadísticos:</th>";

    if(test == "bonferroni"){
        $.each(data.valores_t, function(index, value) {
		    salida = salida + "<td>" + value.toFixed(3) + "</td>";
	    });
	}
    else{
        $.each(data.valores_z, function(index, value) {
		    salida = salida + "<td>" + value.toFixed(3) + "</td>";
	    });
    }

    salida = salida + "</tr><tr><th>p-valores:</th>";

	$.each(data.p_valores, function(index, value) {
		salida = salida + "<td>" + value.toFixed(3) + "</td>";
	});

    salida = salida + "</tr><tr><th>p-valores Ajustados:</th>";

	$.each(data.p_valores_ajustados, function(index, value) {
		salida = salida + "<td>" + value.toFixed(3) + "</td>";
	});

    salida = salida + "</tr><tr><th>Resultados:</th>";

    $.each(data.resultado, function(index, value) {
		if(value == true)
            salida = salida + "<td>Se rechaza H0</td>";
        else
            salida = salida + "<td>Se acepta H0</td>";
	});

    salida = salida + "</tbody></table></div>";
    
    return salida;
}
