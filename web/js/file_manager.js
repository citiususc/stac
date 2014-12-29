$(document).ready(function() {
	$(document).on('click', '#upload_file', function() {
		var formData = new FormData($('#formfile')[0]);
		var fichero = $("#file").val();
		
		$('#info_file').html("Loading...");
		
		if(!fichero)
			$('#info_file').html("<br><p style=\"color:red\";><strong>Select a file</strong></p>");
		else {
			$.ajax({
				type: "POST",
				url: APP_CONFIG.api_url + "/file",
				dataType: "json",
				data: formData,
				cache: false,
				contentType: false,
				processData: false,
				success : function(data) {
					resultado = "";
					if(!data.fallo){
						resultado = "<p style=\"color:green\";><strong>Fichero subido con éxito</strong></p>";
						sessionStorage.setItem("data", data.hash);
						console.log(data);
						sessionStorage.setItem("homocedasticity", false);
						sessionStorage.setItem("normality", false);
						$("#show_file").show();
						$('#info_file').html("Done!");
						
						window.location = APP_CONFIG.app_url + "/file.html";
					} else{
						resultado = resultado + "<p style=\"color:red\";><strong>" + data.fallo + "</strong></p>";
						$('#info_file').html("<br>"+resultado);
						$('#formfile').trigger('reset');
					}
				},
				error : function(e) {
					console.log(e);
				}
			});
		}
	});
	
	if ($(document).find("#file_table").length > 0) {
		show_file();
	}
});

function show_file() {
	var hash = sessionStorage.getItem("data");

	$.ajax({
		type: "GET",
		url: APP_CONFIG.api_url + "/file/"+hash,
		success : function(data) {
			if(data.fallo) {
				$("#danger").html("There is no file uploaded.").show();
			} else {
				var salida = "<thead><tr><th>" + data.palabra + "</th>";
    
				$.each(data.nombres_algoritmos, function(index, value) {
					salida = salida + "<th>" + value + "</th>";
				});

				salida = salida + "</tr></thead><tbody>";
				$.each(data.nombres_conj_datos, function(index, value) {
					salida = salida + "<tr><td>" + value + "</td>";
					$.each(data.matriz_datos[index], function(index, value) {
						salida = salida + "<td>" + value + "</td>";
					});
					salida = salida + "</tr>";
				});

				salida = salida + "</tbody>";
				
				$('#file_table').html(salida);
			}
		},
		error : function(e) {
			console.log('Error: ' + e);
		}
	});
}

