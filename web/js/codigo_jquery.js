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
                url = window.location.origin+"/stac/api/levene/"+sessionStorage.getItem("fichero_actual")+"/"+alpha;
            else
                url = window.location.origin+"/stac/api/levene/"+sessionStorage.getItem("fichero_actual");

            var salida;

            $.ajax({
                type: "GET",
                url: url,
                dataType: "json",
                success : function(data) {
                    salida = "<br><u>Levene test result (homocedasticity):</u>";

                    $("#alerta_fichero_homocedasticidad").hide();

                    if(data.fallo){
                        if(data.fallo.indexOf("fichero") > -1)
                            $("#alerta_fichero_homocedasticidad").show();
                        else
                            $("#fallo_test_homocedasticidad").html(data.fallo).show();
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
                url = window.location.origin+"/stac/api/"+test+"/"+sessionStorage.getItem("fichero_actual")+"/"+alpha;
            else
                url = window.location.origin+"/stac/api/"+test+"/"+sessionStorage.getItem("fichero_actual");

            var salida;

            $.ajax({
                type: "GET",
                url: url,
                dataType: "json",
                success : function(data) {
                    var nombre = $('label[name="test_cond"].active').text();
                    salida = "<br><u>"+nombre+" test result:</u>";

                    $("#alerta_fichero").hide();

                    if(data.fallo){
                        if(data.fallo.indexOf("fichero") > -1)
                            $("#alerta_fichero").show();
                        else
                            $("#fallo_test").html(data.fallo).show();
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
                url = window.location.origin+"/stac/api/anova/"+sessionStorage.getItem("fichero_actual")+"/"+alpha;
            else
                url = window.location.origin+"/stac/api/anova/"+sessionStorage.getItem("fichero_actual");

            $.ajax({
                type: "GET",
                url: url,
                dataType: "json",
                success : function(data) {
                    salida = salida + "<br><u>ANOVA test result:</u>";
                
                    $("#fallo_test").hide();
                    $("#alerta_fichero").hide();
    
                    if(data.fallo){
                        $("#alerta_fichero").show();
                    }
                    else{
                        /*------------Avisos condiciones paramétricas.-----------*/
                        if(sessionStorage.getItem("homocedasticidad") == "no" && sessionStorage.getItem("normalidad") == "no")
                            salida = salida + "<br><br><p class=\"alert alert-info alert-danger\">No parametric conditions test applied. Results may be unreliable.</p>";
                        else if(sessionStorage.getItem("homocedasticidad") == "no")
                            salida = salida + "<br><br><p class=\"alert alert-info alert-danger\">No homocedasticity test applied. Results may be unreliable.</p>";
                        else if(sessionStorage.getItem("normalidad") == "no")
                            salida = salida + "<br><br><p class=\"alert alert-info alert-danger\">No normality test applied. Results may be unreliable.</p>";
                        else if(sessionStorage.getItem("homocedasticidad") == "no_cumple" || sessionStorage.getItem("normalidad") == "no_cumple")
                            salida = salida + "<br><br><p class=\"alert alert-info alert-danger\">Homoscedasticity and normality test statistically not significant at significance levels provided. Results may be unreliable.</p>";
                        /*--------------------------------------------------------*/
                        salida = salida + generar_tabla_parametricos(data.test_anova,"anova");
                        salida = salida + "<br><u>Bonferroni POST-HOC test result:</u>";
                        if(!data.test_comparacion){
                            salida = salida + "<p>The ranking test is not statistically significant</p>";
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
                url = window.location.origin+"/stac/api/ttest/"+sessionStorage.getItem("fichero_actual")+"/"+alpha;
            else
                url = window.location.origin+"/stac/api/ttest/"+sessionStorage.getItem("fichero_actual");

            $.ajax({
                type: "GET",
                url: url,
                dataType: "json",
                success : function(data) {
                    salida = salida + "<br><u>T-test result:</u>";
                
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
                            salida = salida + "<br><br><p class=\"alert alert-info alert-danger\">No parametric conditions test applied. Results may be unreliable.</p>";
                        else if(sessionStorage.getItem("homocedasticidad") == "no")
                            salida = salida + "<br><br><p class=\"alert alert-info alert-danger\">No homocedasticity test applied. Results may be unreliable.</p>";
                        else if(sessionStorage.getItem("normalidad") == "no")
                            salida = salida + "<br><br><p class=\"alert alert-info alert-danger\">No normality test applied. Results may be unreliable.</p>";
                        else if(sessionStorage.getItem("homocedasticidad") == "no_cumple" || sessionStorage.getItem("normalidad") == "no_cumple")
                            salida = salida + "<br><br><p class=\"alert alert-info alert-danger\">Homoscedasticity and normality test statistically not significant at significance levels provided. Results may be unreliable.</p>";
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
                url = window.location.origin+"/stac/api/wilcoxon/"+sessionStorage.getItem("fichero_actual")+"/"+alpha;
            else
                url = window.location.origin+"/stac/api/wilcoxon/"+sessionStorage.getItem("fichero_actual");

            var salida = "";
        
            $.ajax({
                type: "GET",
                url: url,
                dataType: "json",

                success : function(data) {
                    salida = "<br><u>Wilcoxon test result:</u>";
                
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
        var alpha = $('#alpha_ranking').val();
        var tipo = $('input[name=tipo]:checked').val();
        var test_post_hoc = $('input[name=post_hoc]:checked').val();

        if(test_post_hoc === undefined)
            test_post_hoc = "no";

        if(sessionStorage.getItem("fichero_actual") == null)
            $("#alerta_fichero_ranking").show();
        else{
            
            var url;
            
            if(alpha != "no" && tipo != "no" && test_post_hoc != "no")
                url = window.location.origin+"/stac/api/"+test+"/"+sessionStorage.getItem("fichero_actual")+"/"+alpha+"/"+tipo+"/"+test_post_hoc;
            else if(test_post_hoc != "no" && alpha != "no")
                url = window.location.origin+"/stac/api/"+test+"/"+sessionStorage.getItem("fichero_actual")+"/"+alpha+"/"+test_post_hoc;
            else if(test_post_hoc != "no" && tipo != "no")
                url = window.location.origin+"/stac/api/"+test+"/"+sessionStorage.getItem("fichero_actual")+"/"+tipo+"/"+test_post_hoc;
            else if(test_post_hoc != "no")
                url = window.location.origin+"/stac/api/"+test+"/"+sessionStorage.getItem("fichero_actual")+"/"+test_post_hoc;
            else if(alpha != "no" & tipo !="no")
                url = window.location.origin+"/stac/api/"+test+"/"+sessionStorage.getItem("fichero_actual")+"/"+alpha+"/"+tipo;
            else if(alpha != "no")
                url = window.location.origin+"/stac/api/"+test+"/"+sessionStorage.getItem("fichero_actual")+"/"+alpha;
            else if(tipo != "no")
                url = window.location.origin+"/stac/api/"+test+"/"+sessionStorage.getItem("fichero_actual")+"/"+tipo;
            else
                url = window.location.origin+"/stac/api/"+test+"/"+sessionStorage.getItem("fichero_actual");

            var salida = "";
        
            $.ajax({
                type: "GET",
                url: url,
                dataType: "json",

                success : function(data) {
                    var nombre_ranking = $('label[name="nombre_test"].active').text();
                    var nombre_post = $('label[name="nombre_post"].active').text();
                    salida = salida + "<br><u>"+nombre_ranking+" test result:</u>";

                    $("#alerta_fichero_ranking").hide();

                    if(data.fallo){
                        $("#alerta_fichero_ranking").show();
                    }
                    else{
                        salida = salida + generar_tabla_ranking(data.test_ranking)
                        salida = salida + "<br><u>"+nombre_post+" test result:</u>";
                        if(!data.test_comparacion){
                            salida = salida + "<p>The ranking test is not statistically significant.</p>";
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
            $('#mensaje_subida').html("<br><p style=\"color:red\";><strong>Select a file</strong></p>");
        else{
            $.ajax({
                type: "POST",
                url: window.location.origin+"/stac/api/fichero",
                dataType: "json",
                data: formData,
                cache: false,
                contentType: false,
                processData: false,
                success : function(data) {
                    resultado = "";
                    if(!data.fallo){
                        //resultado = "<p style=\"color:green\";><strong>Fichero subido con éxito</strong></p>";
						sessionStorage.setItem("fichero_actual", data.clave);
                        sessionStorage.setItem("homocedasticidad", "no");
                        sessionStorage.setItem("normalidad", "no");
                        $("#mostrar_consulta_fichero").show();
                        window.location.replace("/stac/consultar_fichero.html");
					}
                    else{
                        resultado = resultado + "<p style=\"color:red\";><strong>" + data.fallo + "</strong></p>";
                        $('#mensaje_subida').html("<br>"+resultado);
                        $('#formfichero').trigger('reset');
                    }
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

});


//Función para exportar archivos .csv
function exportTableToCSV($table, filename) {

    var $rows = $table.find('tr:has(th,td)'),

        // Temporary delimiter characters unlikely to be typed by keyboard
        // This is to avoid accidentally splitting the actual contents
        tmpColDelim = String.fromCharCode(11), // vertical tab character
        tmpRowDelim = String.fromCharCode(0), // null character

        // actual delimiter characters for CSV format
        colDelim = '","',
        rowDelim = '"\r\n"',

        // Grab text from table into CSV formatted string
        csv = '"' + $rows.map(function (i, row) {
            var $row = $(row),
                $cols = $row.find('th,td');

            return $cols.map(function (j, col) {
                var $col = $(col),
                    text = $col.text();

                return text.replace('"', '""'); // escape double quotes

            }).get().join(tmpColDelim);

        }).get().join(tmpRowDelim)
            .split(tmpRowDelim).join(rowDelim)
            .split(tmpColDelim).join(colDelim) + '"',

        // Data URI
        csvData = 'data:application/csv;charset=utf-8,' + encodeURIComponent(csv);

    if(navigator.appName == 'Microsoft Internet Explorer'){
        var generator = window.open(filename, 'csv', 'height=400,width=600');
        generator.document.write('<html><head><title>CSV</title>');
        generator.document.write('</head><body >');
        generator.document.write('<textArea cols=70 rows=15 wrap="off" >');
        generator.document.write(csv);
        generator.document.write('</textArea>');
        generator.document.write('</body></html>');
        generator.document.close();
    }
    else{
        $(this).attr({
            'download': filename,
            'href': csvData,
            'target': '_blank'
        });
    }
}

//Función para exportar archivos .tex
function exportTableToLaTeX($table, filename) {

    /*Función para repetir un string un determinado número de veces.*/
    String.prototype.repeat = function (n, d) {
        return --n ? this + (d || "") + this.repeat(n, d) : "" + this;
    };

    var $firstrow = $table.find('tr:has(th)'),

        // Temporary delimiter characters unlikely to be typed by keyboard
        // This is to avoid accidentally splitting the actual contents
        tmpColDelim = String.fromCharCode(11), // vertical tab character
        tmpRowDelim = String.fromCharCode(0), // null character

        // Actual delimiter characters for LaTeX format
        colDelim = "&",
        rowDelim = "\\\\\n",

        /*Primera línea de la tabla LaTeX.*/
        latex = "\\begin{tabular}{"+"c".repeat($firstrow.find('th').length,"|")+"}\n",

        latex = latex + $firstrow.map(function (i, row) {
            var $row = $(row),
                $cols = $row.find('th');
            return $cols.map(function (j, col) {
                var $col = $(col),
                    text = $col.text();
                return text;
            }).get().join(tmpColDelim);
        }).get().join(tmpRowDelim)
                .split(tmpRowDelim).join(rowDelim)
                .split(tmpColDelim).join(colDelim);

        latex = latex + "\\\\\n\\hline\n",

        /*Resto de líneas de la tabla LaTeX.*/
        $rows = $table.find('tr:has(td)'),

        latex = latex + $rows.map(function (i, row) {
            var $row = $(row),
                $cols = $row.find('td');
            return $cols.map(function (j, col) {
                var $col = $(col),
                    text = $col.text();
                return text;
            }).get().join(tmpColDelim);
        }).get().join(tmpRowDelim)
                .split(tmpRowDelim).join(rowDelim)
                .split(tmpColDelim).join(colDelim);

        /*Última línea de la tabla LaTeX.*/
        latex = latex + "\n\\end{tabular}",

        // Data URI
        latexData = 'data:application/octet-stream;charset=utf-8,' + encodeURIComponent(latex);

    if(navigator.appName == 'Microsoft Internet Explorer'){
        var generator = window.open(filename, 'latex', 'height=400,width=600');
        generator.document.write('<html><head><title>LaTeX</title>');
        generator.document.write('</head><body >');
        generator.document.write('<textArea cols=70 rows=15 wrap="off" >');
        generator.document.write(latex);
        generator.document.write('</textArea>');
        generator.document.write('</body></html>');
        generator.document.close();
    }
    else{
        $(this).attr({
            'download': filename,
            'href': latexData,
            'target': '_blank'
        });
    }
}

//Función javascript para generar la tabla de resultados para los tests paramétricos de Anova y T-test.
function generar_tabla_parametricos(data,test) {

    var salida = "<div id=\"parametricos\" class=\"table-responsive\"><br>";

    //Botón para exportar a .csv y a .tex
    if(test == "anova")
        salida = salida + "<a href=\"#\" onclick=\"exportTableToCSV.apply(this, [$('#parametricos'), 'anova_test.csv'])\"><button class=\"btn btn-default\">Export to csv</button></a>&nbsp;&nbsp;<a href=\"#\" onclick=\"exportTableToLaTeX.apply(this, [$('#parametricos'), 'anova_test.tex'])\"><button class=\"btn btn-default\">Export to LaTeX</button></a>";
    else
        salida = salida + "<a href=\"#\" onclick=\"exportTableToCSV.apply(this, [$('#parametricos'), 'ttest.csv'])\"><button class=\"btn btn-default\">Export to csv</button></a>&nbsp;&nbsp;<a href=\"#\" onclick=\"exportTableToLaTeX.apply(this, [$('#parametricos'), 'ttest.tex'])\"><button class=\"btn btn-default\">Export to LaTeX</button></a>";

    salida = salida + "<br><br><table class=\"table table-hover\">";

    if(test == "anova"){
        salida = salida + "<thead><tr><th>Statistic</th><th>p-value</th><th>Result</th></tr></thead>";
        salida = salida + "<tbody><tr><td>" +data.estadistico.toFixed(3)+ "</td>";
    }    
    else{
        salida = salida + "<thead><tr><th>T Statistic</th><th>p-value</th><th>Result</th></tr></thead>";
        salida = salida + "<tbody><tr><td>" +data.estadistico_t.toFixed(3)+ "</td>";
    }
    salida = salida + "<td>" +data.p_valor.toFixed(3)+ "</td>";
    if(data.resultado == true)
        salida = salida + "<td>H0 is rejected</td></tr></tbody></table>";
    else
        salida = salida + "<td>H0 is accepted</td></tr></tbody></table>";
    
    //Ayuda.
    salida = salida + "<a href=\"ayuda.html#collapseTwo\" id=\"ayuda_fichero\" target=\"_blank\">Go help.</a></div>";

    return salida;
}

//Función javascript para generar la tabla de resultados para el test de condición de homocedasticidad de Levene.
function generar_tabla_levene(data) {

    var salida = "<div class=\"table-responsive\"><br>";

    //Botón para exportar a .csv y a .tex
    salida = salida + "<a href=\"#\" onclick=\"exportTableToCSV.apply(this, [$('table'), 'levene_test.csv'])\"><button class=\"btn btn-default\">Export to csv</button></a>&nbsp;&nbsp;<a href=\"#\" onclick=\"exportTableToLaTeX.apply(this, [$('table'), 'levene_test.tex'])\"><button class=\"btn btn-default\">Export to LaTeX</button></a>";

    salida = salida + "<br><br><table class=\"table table-hover\"><thead>";
    salida = salida + "<tr><th>W Statistic</th><th>p-value</th><th>Result</th></tr></thead>";
    salida = salida + "<tbody><tr><td>" +data.estadistico_w.toFixed(3)+ "</td><td>" +data.p_valor.toFixed(3)+ "</td>";
    if(data.resultado == true)
        salida = salida + "<td>H0 is rejected</td></tr></tbody></table>";
    else
        salida = salida + "<td>H0 is accepted</td></tr></tbody></table>";
    
    //Ayuda.
    salida = salida + "<a href=\"ayuda.html#collapseTwo\" id=\"ayuda_fichero\" target=\"_blank\">Go help.</a></div>";

    return salida;
}

//Función javascript para generar la tabla de resultados de los tests de condición de normalidad.
function generar_tabla_normalidad(data, test) {

    var salida = "<div class=\"table-responsive\"><br>";

    //Botón para exportar a .csv y a .tex
    salida = salida + "<a href=\"#\" onclick=\"exportTableToCSV.apply(this, [$('table'), $('input[name=test]:checked').val()+'.csv'])\"><button class=\"btn btn-default\">Export to csv</button></a>&nbsp;&nbsp;<a href=\"#\" onclick=\"exportTableToLaTeX.apply(this, [$('table'), $('input[name=test]:checked').val()+'.tex'])\"><button class=\"btn btn-default\">Export to LaTeX</button></a>";

    //Primera fila de la tabla.
    salida = salida + "<br><br><table class=\"table table-hover\"><thead><tr><th>Dataset</th>";
    
    if(test == "shapiro"){
        salida = salida + "<th>W Statistics</th><th>p-values</th><th>Results</th></tr></thead><tbody>";
        $.each(data.p_valores, function(index, value) {
		    salida = salida + "<tr><td>" + (index+1) + "</td><td>" + data.estadisticos_w[index].toFixed(3) + "</td><td>" + data.p_valores[index].toFixed(3) + "</td>";
            if(data.resultado[index] == true)
                salida = salida + "<td>H0 is rejected</td></tr>";
            else
                salida = salida + "<td>H0 is accepted</td></tr>";
	        });
    }
    else if(test == "kolmogorov"){
        salida = salida + "<th>D Statistics</th><th>p-values</th><th>Results</th></tr></thead><tbody>";
        $.each(data.p_valores, function(index, value) {
		    salida = salida + "<tr><td>" + (index+1) + "</td><td>" + data.estadisticos_d[index].toFixed(3) + "</td><td>" + data.p_valores[index].toFixed(3) + "</td>";
            if(data.resultado[index] == true)
                salida = salida + "<td>H0 is rejected</td></tr>";
            else
                salida = salida + "<td>H0 is accepted</td></tr>";
	        });
    }
    else{
        salida = salida + "<th>K2 Statistics</th><th>p-values</th><th>Results</th></tr></thead><tbody>";
        $.each(data.p_valores, function(index, value) {
		    salida = salida + "<tr><td>" + (index+1) + "</td><td>" + data.estadisticos_k2[index].toFixed(3) + "</td><td>" + data.p_valores[index].toFixed(3) + "</td>";
            if(data.resultado[index] == true)
                salida = salida + "<td>H0 is rejected</td></tr>";
            else
                salida = salida + "<td>H0 is accepted</td></tr>";
	        });
    }

	salida = salida + "</tbody></table>";

    //Ayuda.
    salida = salida + "<a href=\"ayuda.html#collapseTwo\" id=\"ayuda_fichero\" target=\"_blank\">Go help.</a></div>";

    return salida;
}

//Función javascript para generar la tabla de resultados del test de Wilcoxon.
function generar_tabla_wilcoxon(data) {

    var salida = "<div class=\"table-responsive\"><br>";

    //Botón para exportar a .csv y a .tex
    salida = salida + "<a href=\"#\" onclick=\"exportTableToCSV.apply(this, [$('table'), 'wilcoxon_test.csv'])\"><button class=\"btn btn-default\">Export to csv</button></a>&nbsp;&nbsp;<a href=\"#\" onclick=\"exportTableToLaTeX.apply(this, [$('table'), 'wilcoxon_test.tex'])\"><button class=\"btn btn-default\">Export to LaTeX</button></a>";

    salida = salida + "<br><br><table class=\"table table-hover\"><thead>";
    if(data.p_valor){
        salida = salida + "<tr><th>Statistic</th><th>p-value</th><th>Sum of positive ranks</th><th>Sum of negative ranks</th><th>Result</th></tr></thead>";
        salida = salida + "<tbody><tr><td>" +data.estadistico.toFixed(3)+ "</td><td>" +data.p_valor.toFixed(3)+ "</td><td>" +data["suma rangos pos"]+ "</td><td>" +data["suma rangos neg"]+ "</td>";
    }
    else{
        salida = salida + "<tr><th>Statistic</th><th>Critical point</th><th>Sum of positive ranks</th><th>Sum of negative ranks</th><th>Result</th></tr></thead>";
        salida = salida + "<tbody><tr><td>" +data.estadistico+ "</td><td>" +data["punto critico"]+ "</td><td>" +data["suma rangos pos"]+ "</td><td>" +data["suma rangos neg"]+ "</td>";
    }
    if(data.resultado == true)
        salida = salida + "<td>H0 is rejected</td></tr></tbody></table>";
    else
        salida = salida + "<td>H0 is accepted</td></tr></tbody></table>";
    
    //Ayuda.
    salida = salida + "<a href=\"ayuda.html#collapseTwo\" id=\"ayuda_fichero\" target=\"_blank\">Go help.</a></div>";

    return salida;
}

//Función javascript para generar la tabla de resultados de los tests de ranking.
function generar_tabla_ranking(data) {

    var salida = "<div id=\"result_ranking\" class=\"table-responsive\"><br>";

    //Botón para exportar a .csv y a .tex
    salida = salida + "<a href=\"#\" onclick=\"exportTableToCSV.apply(this, [$('#result_ranking'), $('input[name=test]:checked').val()+'.csv'])\"><button class=\"btn btn-default\">Export to csv</button></a>&nbsp;&nbsp;<a href=\"#\" onclick=\"exportTableToLaTeX.apply(this, [$('#result_ranking'), $('input[name=test]:checked').val()+'.tex'])\"><button class=\"btn btn-default\">Export to LaTeX</button></a>";

    salida = salida + "<br><br><table class=\"table table-hover\"><thead>";
    salida = salida + "<tr><th>Ranking</th><th>Algorithms</th><th>Statistic</th><th>p-value</th><th>Result:</th></tr></thead><tbody>";
    $.each(data.ranking, function(index, value) {
        if(index==0){
		    salida = salida + "<tr><td>" + value.toFixed(3) + "</td><td>" + data.nombres[index] + "</td><td>" + data.estadistico.toFixed(3) + "</td><td>" + data.p_valor.toFixed(3) + "</td>";
            if(data.resultado == true)
                salida = salida + "<td>H0 is rejected</td></tr>";
            else
                salida = salida + "<td>H0 is accepted</td></tr>";
        }
        else
            salida = salida + "<tr><td>" + value.toFixed(3) + "</td><td>" + data.nombres[index] + "</td><td>-</td><td>-</td><td>-</td></tr>";
	});

    salida = salida + "</tbody></table>";
    
    //Ayuda.
    salida = salida + "<a href=\"ayuda.html#collapseTwo\" id=\"ayuda_fichero\" target=\"_blank\">Go help.</a></div>";

    return salida;
}

//Función javascript para generar la tabla de resultados de los tests Post-Hoc con método de control.
function generar_tabla_control(data, test) {

    var salida = "<div id=\"post_hoc_metodoc\" class=\"table-responsive\"><br>";

    //Botón para exportar a .csv y a .tex
    salida = salida + "<a href=\"#\" onclick=\"exportTableToCSV.apply(this, [$('#post_hoc_metodoc'), $('input[name=post_hoc]:checked').val()+'.csv'])\"><button class=\"btn btn-default\">Export to csv</button></a>&nbsp;&nbsp;<a href=\"#\" onclick=\"exportTableToLaTeX.apply(this, [$('#post_hoc_metodoc'), $('input[name=post_hoc]:checked').val()+'.tex'])\"><button class=\"btn btn-default\">Export to LaTeX</button></a>";

    salida = salida + "<br><br><table class=\"table table-hover\"><thead>";
    if(test != "li_test")
        salida = salida + "<tr><th>Control Method</th><th>Adjusted alpha</th><th>Control Method VS</th><th>Statistic</th><th>p-value</th><th>Adjusted p-value</th><th>Result</th></tr></thead><tbody>";
    else
        salida = salida + "<tr><th>Control Method</th><th>Control Method VS</th><th>Statistic</th><th>p-value</th><th>Adjusted p-value</th><th>Result</th></tr></thead><tbody>";
    if(test == "no" || test == "bonferroni_dunn_test"){
        salida = salida + "<tr><td>" +data.metodo_control+ "</td><td>" +data.alpha.toFixed(3)+ "</td>";
        $.each(data.nombres, function(index, value) {
            if(index==0)
                salida = salida + "<td>" +value+ "</td><td>" +data.valores_z[index].toFixed(3)+ "</td><td>" +data.p_valores[index].toFixed(3)+ "</td><td>" +data.p_valores_ajustados[index].toFixed(3)+ "</td>";
            else
                salida = salida + "<tr><td>-</td><td>-</td><td>" +value+ "</td><td>" +data.valores_z[index].toFixed(3)+ "</td><td>" +data.p_valores[index].toFixed(3)+ "</td><td>" +data.p_valores_ajustados[index].toFixed(3)+ "</td>";
            if(data.resultado[index] == true)
                salida = salida + "<td>H0 is rejected</td></tr>";
            else
                salida = salida + "<td>H0 is accepted</td></tr>";
	        
        });
    }
    else{
        salida = salida + "<tr><td>" +data.metodo_control+ "</td>";
        $.each(data.nombres, function(index, value) {
            if(test != "li_test"){
                if(index==0)
                    salida = salida + "<td>" +data.alphas[index].toFixed(3)+ "</td><td>" +value+ "</td><td>" +data.valores_z[index].toFixed(3)+ "</td><td>" +data.p_valores[index].toFixed(3)+ "</td><td>" +data.p_valores_ajustados[index].toFixed(3)+ "</td>";
                else
                    salida = salida + "<td>-</td><td>" +data.alphas[index].toFixed(3)+ "</td><td>" +value+ "</td><td>" +data.valores_z[index].toFixed(3)+ "</td><td>" +data.p_valores[index].toFixed(3)+ "</td><td>" +data.p_valores_ajustados[index].toFixed(3)+ "</td>";
            }
            else{
                if(index==0)
                    salida = salida + "<td>" +value+ "</td><td>" +data.valores_z[index].toFixed(3)+ "</td><td>" +data.p_valores[index].toFixed(3)+ "</td><td>" +data.p_valores_ajustados[index].toFixed(3)+ "</td>";
                else
                    salida = salida + "<td>-</td><td>" +value+ "</td><td>" +data.valores_z[index].toFixed(3)+ "</td><td>" +data.p_valores[index].toFixed(3)+ "</td><td>" +data.p_valores_ajustados[index].toFixed(3)+ "</td>";
            }
            if(data.resultado[index] == true)
                salida = salida + "<td>H0 is rejected</td></tr>";
            else
                salida = salida + "<td>H0 is accepted</td></tr>";
        });
    }

    salida = salida + "</tbody></table>";
    
    //Ayuda.
    salida = salida + "<a href=\"ayuda.html#collapseTwo\" id=\"ayuda_fichero\" target=\"_blank\">Go help.</a></div>";

    return salida;
}

//Función javascript para generar la tabla de resultados de los tests Post-Hoc multitests.
function generar_tabla_multitests(data, test) {

    var salida = "<div id=\"post_hoc_multi\" class=\"table-responsive\"><br>";

    //Botón para exportar a .csv
    if(test == "bonferroni")
        salida = salida + "<a href=\"#\" onclick=\"exportTableToCSV.apply(this, [$('#post_hoc_multi'), 'bonferroni.csv'])\"><button class=\"btn btn-default\">Export to csv</button></a>&nbsp;&nbsp;<a href=\"#\" onclick=\"exportTableToLaTeX.apply(this, [$('#post_hoc_multi'), 'bonferroni.tex'])\"><button class=\"btn btn-default\">Export to LaTeX</button></a>";
    else
        salida = salida + "<a href=\"#\" onclick=\"exportTableToCSV.apply(this, [$('#post_hoc_multi'), $('input[name=post_hoc]:checked').val()+'.csv'])\"><button class=\"btn btn-default\">Export to csv</button></a>&nbsp;&nbsp;<a href=\"#\" onclick=\"exportTableToLaTeX.apply(this, [$('#post_hoc_multi'), $('input[name=post_hoc]:checked').val()+'.tex'])\"><button class=\"btn btn-default\">Export to LaTeX</button></a>";

    salida = salida + "<br><br><table class=\"table table-hover\"><thead>";
    salida = salida + "<tr><th>Adjusted alpha</th><th>Comparison</th><th>Statistic</th><th>p-value</th><th>Adjusted p-value</th><th>Result</th></tr></thead><tbody>";
    if(test == "nemenyi_multitest"){
        salida = salida + "<tr><td>" +data.alpha.toFixed(3)+ "</td>";
        $.each(data.comparaciones, function(index, value) {
            if(index==0)
	            salida = salida + "<td>" + value + "</td><td>" +data.valores_z[index].toFixed(3)+ "</td><td>" +data.p_valores[index].toFixed(3)+ "</td><td>" +data.p_valores_ajustados[index].toFixed(3)+ "</td>";
            else
                salida = salida + "<td>-</td><td>" + value + "</td><td>" +data.valores_z[index].toFixed(3)+ "</td><td>" +data.p_valores[index].toFixed(3)+ "</td><td>" +data.p_valores_ajustados[index].toFixed(3)+ "</td>";
            if(data.resultado[index] == true)
                salida = salida + "<td>H0 is rejected</td></tr>";
            else
                salida = salida + "<td>H0 is accepted</td></tr>";
        });
    }
    else if(test == "bonferroni"){
        salida = salida + "<tr><td>" +data.alpha.toFixed(3)+ "</td>";
        $.each(data.comparaciones, function(index, value) {
            if(index==0)
                salida = salida + "<td>" + value + "</td><td>" +data.valores_t[index].toFixed(3)+ "</td><td>" +data.p_valores[index].toFixed(3)+ "</td><td>" +data.p_valores_ajustados[index].toFixed(3)+ "</td>";
            else
                salida = salida + "<td>-</td><td>" + value + "</td><td>" +data.valores_t[index].toFixed(3)+ "</td><td>" +data.p_valores[index].toFixed(3)+ "</td><td>" +data.p_valores_ajustados[index].toFixed(3)+ "</td>";
            if(data.resultado[index] == true)
                salida = salida + "<td>H0 is rejected</td></tr>";
            else
                salida = salida + "<td>H0 is accepted</td></tr>";
        });
    }
    else{
        $.each(data.alphas, function(index, value) {
	        salida = salida + "<td>" + value.toFixed(3) + "</td><td>" +data.comparaciones[index]+ "</td><td>" +data.valores_z[index].toFixed(3)+ "</td><td>" +data.p_valores[index].toFixed(3)+ "</td><td>" +data.p_valores_ajustados[index].toFixed(3)+ "</td>";
            if(data.resultado[index] == true)
                salida = salida + "<td>H0 is rejected</td></tr>";
            else
                salida = salida + "<td>H0 is accepted</td></tr>";
        });
    }
    
    salida = salida + "</tbody></table>";
    
    //Ayuda.
    salida = salida + "<a href=\"ayuda.html#collapseTwo\" id=\"ayuda_fichero\" target=\"_blank\">Go help.</a></div>";

    return salida;
}


