$(document).on('ready', function() {

    //Para mostrar "Consultar fichero" en caso de que halla algún fichero subido.
    if(sessionStorage.getItem("fichero_actual") != null)
        $("#mostrar_consulta_fichero").show();

	//Para obtener la url base. Compatible con los navegadores: Chrome 27, Firefox 23, Safari 6, Internet Explorer 10.
	if (!window.location.origin)
 		window.location.origin = window.location.protocol+"//"+window.location.host;

    //Ejecución del test de Levene para comprobar el criterio de homocedasticidad.
    $(document).on('click', '#datos_homocedasticidad', function() {

        var alpha = $('#alpha_homocedasticidad').val();

        if(sessionStorage.getItem("fichero_actual") == null)
            $("#alerta_fichero_homocedasticidad").show();
        else{

            var url;
            if(alpha != "no")
                url = window.location.origin+"/stac/beta/api/levene/"+sessionStorage.getItem("fichero_actual")+"/"+alpha;
            else
                url = window.location.origin+"/stac/beta/api/levene/"+sessionStorage.getItem("fichero_actual");

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
                            sessionStorage.setItem("homocedasticidad", "cumple");
                        else
                            sessionStorage.setItem("homocedasticidad", "no_cumple");
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

        if(sessionStorage.getItem("fichero_actual") == null)
            $("#alerta_fichero").show();
        else{

            var url;
            if(alpha != "no")
                url = window.location.origin+"/stac/beta/api/"+test+"/"+sessionStorage.getItem("fichero_actual")+"/"+alpha;
            else
                url = window.location.origin+"/stac/beta/api/"+test+"/"+sessionStorage.getItem("fichero_actual");

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
                            sessionStorage.setItem("normalidad", "no_cumple");
                        else
                            sessionStorage.setItem("normalidad", "cumple");
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
        var salida = "";

        if(sessionStorage.getItem("fichero_actual") == null)
            $("#alerta_fichero").show();
        
        else{

            var url;
            if(alpha != "no")
                url = window.location.origin+"/stac/beta/api/anova/"+sessionStorage.getItem("fichero_actual")+"/"+alpha;
            else
                url = window.location.origin+"/stac/beta/api/anova/"+sessionStorage.getItem("fichero_actual");

            $.ajax({
                type: "GET",
                url: url,
                dataType: "json",
                success : function(data) {
                    salida = salida + "<br><u>Resultado test ANOVA:</u>";
                
                    $("#fallo_test").hide();
                    $("#alerta_fichero").hide();
    
                    if(data.fallo){
                        $("#alerta_fichero").show();
                    }
                    else{
                        /*------------Avisos condiciones paramétricas.-----------*/
                        if(sessionStorage.getItem("homocedasticidad") == "no" && sessionStorage.getItem("normalidad") == "no")
                            salida = salida + "<br><br><p class=\"alert alert-info alert-danger\">No se han aplicado los tests de condiciones paramétricas. Puede que los resultados no sean fiables.</p>";
                        else if(sessionStorage.getItem("homocedasticidad") == "no")
                            salida = salida + "<br><br><p class=\"alert alert-info alert-danger\">No se ha aplicado el test de condición paramétrica de homocedasticidad. Puede que los resultados no sean fiables.</p>";
                        else if(sessionStorage.getItem("normalidad") == "no")
                            salida = salida + "<br><br><p class=\"alert alert-info alert-danger\">No se ha realizado ningún test de condición paramétrica de normalidad. Puede que los resultados no sean fiables.</p>";
                        else if(sessionStorage.getItem("homocedasticidad") == "no_cumple" || sessionStorage.getItem("normalidad") == "no_cumple")
                            salida = salida + "<br><br><p class=\"alert alert-info alert-danger\">Los datos no cumplen las condiciones paramétricas a los niveles de significancia proporcionados. Puede que los resultados no sean fiables.</p>";
                        /*--------------------------------------------------------*/
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
        var salida = "";

        if(sessionStorage.getItem("fichero_actual") == null)
            $("#alerta_fichero_ttest").show();
        
        else{

            var url;
            if(alpha != "no")
                url = window.location.origin+"/stac/beta/api/ttest/"+sessionStorage.getItem("fichero_actual")+"/"+alpha;
            else
                url = window.location.origin+"/stac/beta/api/ttest/"+sessionStorage.getItem("fichero_actual");

            $.ajax({
                type: "GET",
                url: url,
                dataType: "json",
                success : function(data) {
                    salida = salida + "<br><u>Resultado T-test:</u>";
                
                    $("#fallo_test_ttest").hide();
                    $("#alerta_fichero_ttest").hide();
    
                    if(data.fallo){
                        if(data.fallo.indexOf("fichero") > -1)
                            $("#alerta_fichero_ttest").show();
                        else
                            $("#fallo_test_ttest").html(data.fallo).show();
                    }
                    else{
                        /*------------Avisos condiciones paramétricas.-----------*/
                        if(sessionStorage.getItem("homocedasticidad") == "no" && sessionStorage.getItem("normalidad") == "no")
                            salida = salida + "<br><br><p class=\"alert alert-info alert-danger\">No se han aplicado los tests de condiciones paramétricas. Puede que los resultados no sean fiables.</p>";
                        else if(sessionStorage.getItem("homocedasticidad") == "no")
                            salida = salida + "<br><br><p class=\"alert alert-info alert-danger\">No se ha aplicado el test de condición paramétrica de homocedasticidad. Puede que los resultados no sean fiables.</p>";
                        else if(sessionStorage.getItem("normalidad") == "no")
                            salida = salida + "<br><br><p class=\"alert alert-info alert-danger\">No se ha realizado ningún test de condición paramétrica de normalidad. Puede que los resultados no sean fiables.</p>";
                        else if(sessionStorage.getItem("homocedasticidad") == "no_cumple" || sessionStorage.getItem("normalidad") == "no_cumple")
                            salida = salida + "<br><br><p class=\"alert alert-info alert-danger\">Los datos no cumplen las condiciones paramétricas a los niveles de significancia proporcionados. Puede que los resultados no sean fiables.</p>";
                        /*--------------------------------------------------------*/
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
        
        if(sessionStorage.getItem("fichero_actual") == null)
            $("#alerta_fichero").show();
        else{
            
            var url;
            
            if(alpha != "no")
                url = window.location.origin+"/stac/beta/api/wilcoxon/"+sessionStorage.getItem("fichero_actual")+"/"+alpha;
            else
                url = window.location.origin+"/stac/beta/api/wilcoxon/"+sessionStorage.getItem("fichero_actual");

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

        if(sessionStorage.getItem("fichero_actual") == null)
            $("#alerta_fichero_ranking").show();
        else{
            
            var url;
            
            if(alpha != "no" && tipo != "no" && test_post_hoc != "no")
                url = window.location.origin+"/stac/beta/api/"+test+"/"+sessionStorage.getItem("fichero_actual")+"/"+alpha+"/"+tipo+"/"+test_post_hoc;
            else if(test_post_hoc != "no" && alpha != "no")
                url = window.location.origin+"/stac/beta/api/"+test+"/"+sessionStorage.getItem("fichero_actual")+"/"+alpha+"/"+test_post_hoc;
            else if(test_post_hoc != "no" && tipo != "no")
                url = window.location.origin+"/stac/beta/api/"+test+"/"+sessionStorage.getItem("fichero_actual")+"/"+tipo+"/"+test_post_hoc;
            else if(test_post_hoc != "no")
                url = window.location.origin+"/stac/beta/api/"+test+"/"+sessionStorage.getItem("fichero_actual")+"/"+test_post_hoc;
            else if(alpha != "no" & tipo !="no")
                url = window.location.origin+"/stac/beta/api/"+test+"/"+sessionStorage.getItem("fichero_actual")+"/"+alpha+"/"+tipo;
            else if(alpha != "no")
                url = window.location.origin+"/stac/beta/api/"+test+"/"+sessionStorage.getItem("fichero_actual")+"/"+alpha;
            else if(tipo != "no")
                url = window.location.origin+"/stac/beta/api/"+test+"/"+sessionStorage.getItem("fichero_actual")+"/"+tipo;
            else
                url = window.location.origin+"/stac/beta/api/"+test+"/"+sessionStorage.getItem("fichero_actual");

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
						sessionStorage.setItem("fichero_actual", data.clave);
                        sessionStorage.setItem("homocedasticidad", "no");
                        sessionStorage.setItem("normalidad", "no");
                        $("#mostrar_consulta_fichero").show();
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
    $(document).on('click', '#boton_subida', function() {
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

    /*Despliegue menú para subida de fichero. Se despliega la ventana de subida cuando se hace
    click en #boton_subida o #a_subida y cuando se hace click en cualquier otro lugar de la página
    se cierra la ventana de subida con hide().*/
    $('#boton_subida').click(function() {
        $('.dropdown-menu').show();
    });
    $('#a_subida').click(function() {
        $('.dropdown-menu').show();
    });
    $("body").on("click",function(e) {
        if($(e.target).is('a#boton_subida') || $(e.target).is('a#a_subida') || $(e.target).is('div.dropdown-menu') || 
            $(e.target).closest('div.dropdown-menu').length) {
            //No hago nada.
        }
        else{
            $('.dropdown-menu').hide();
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
