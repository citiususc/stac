$(document).on('ready', function() {

	var fichero = localStorage.getItem("fichero_actual");

	if(fichero!=null) {
        $.ajax({
            type: "GET",
            url: window.location.origin+"/stac/beta/api/fichero/"+fichero,
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
            },
            error : function(e) {
                alert('Error: ' + e);
            }
        });
    }
    else{
        alert("Sube un fichero");
    }

});
