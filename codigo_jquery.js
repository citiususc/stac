$(document).on('ready', function() {

	//Ejecución de los tests.
    $(document).on('click', '#datos', function() {

        var test = $('#test').val();
        var alpha = $('#alpha').val();
        var tipo = $('#tipo').val();
		var id_fichero = $('#selector_fichero').val();

		if(!id_fichero || id_fichero=="no")
			alert("Selecciona un fichero")
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

		    $.ajax({
		        type: "get",
		        url: url,
		        dataType: "json",
		        success : function(data) {
		            salida = "<p>Resultado test:</p>";
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
			   	url: "http://localhost:8080/subir",
				dataType: "json",
				data: formData,
				cache: false,
				contentType: false,
				processData: false,
				success : function(data) {
					if(!data.fallo){
						lista1 = "<p>Lista de ficheros:</p>";
						lista2 = "<select id=\"selector_fichero\"><option value=\"no\">Elige</option>";
				        $.each(data, function(key, val) {
				            lista1 = lista1 + "<input type=\"radio\" name=\"consulta\" value=\"" + key + "\"> " + val + "<br>";
							lista2 = lista2 + "<option value=\"" + key + "\">" + val + "</option>";
				        });
						lista1 = lista1 + "<br><input type=\"button\" value=\"Ver Contenido\" id=\"boton_contenido\"/><br><br>";
						lista2 = lista2 + "</select><br><br>";
						$('#campos').html(lista1);
						$("#error").empty();
						$('#seleccionar_fichero').html(lista2);
					}
					else{
						$.each(data, function(key, val) {
							$('#error').html("<p>" +data.fallo+ "</p>");
						});
					}
					$('#formfichero').trigger('reset');
				},
				error : function(e) {
				    alert('Error: ' + e);
				}
			});
		}

	});

	//Consulta de ficheros.
	$(document).on('click', '#boton_contenido', function() {

		if( $("#seleccion_fichero input[name='consulta']:radio").is(':checked')) {
			var consulta_id = $('input:radio[name=consulta]:checked').val();
			$.ajax({
				type: "GET",
			   	url: "http://localhost:8080/consultar/"+consulta_id,
				success : function(data) {
					salida = "<p>Contenido del fichero:</p>";
		            $.each(data, function(key, val) {
		            	salida = salida + "<p>" + key + " = " + val + "</p>";
		            });
					$('#contenido_fichero').html(salida);
					$('input:radio').prop('checked', false);
				},
				error : function(e) {
				    alert('Error: ' + e);
				}
			});
        }
		else{
        	alert("Selecciona un fichero");
		}

	});

});
