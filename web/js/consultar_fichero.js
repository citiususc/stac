//Consulta de ficheros.
$(document).on('ready', function() {

	var fichero = sessionStorage.getItem("fichero_actual");

	if(fichero!=null) {
        $.ajax({
            type: "GET",
            url: window.location.origin+"/stac/api/fichero/"+fichero,
            success : function(data) {
                if(data.fallo){
                    $("#alerta_fichero").show();
                }
                else{
					salida = generar_tabla(data);
                    $('#contenido_fichero').html(salida);
                }
            },
            error : function(e) {
                alert('Error: ' + e);
            }
        });
    }
    else{
        $("#alerta_fichero").show();
    }

});

/*
Función javascript para generar la tabla a partir del fichero a partir de los datos
devueltos por el servidor (en formato JSON). 
*/ 
function generar_tabla(data) {

    //Primera fila de la tabla.
    var salida = "<thead><tr><th>" + data.palabra + "</th>";
    
	$.each(data.nombres_algoritmos, function(index, value) {
		salida = salida + "<th>" + value + "</th>";
	});

    //Resto de filas de la tabla.
	salida = salida + "</tr></thead><tbody>";
	$.each(data.nombres_conj_datos, function(index, value) {
		salida = salida + "<tr><td>" + value + "</td>";
		$.each(data.matriz_datos[index], function(index, value) {
			salida = salida + "<td>" + value + "</td>";
		});
		salida = salida + "</tr>";
	});

	salida = salida + "</tbody>";

    return salida;
}

