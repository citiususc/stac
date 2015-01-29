$(document).ready(function() {
	$(document).on('click', '#upload_file', function() {
		var formData = new FormData($('#formfile')[0]);
		var fichero = $("#file").val();

        var csvfile = $("#file")[0].files[0];

        Papa.parse(csvfile, {
            header: true,
            dynamicTyping: true,
            complete: function(results) {
                var data = {};
                data["dataset"] = [];
                var key = results.meta.fields[0];
                if (results.data.map(function(row) { return isNaN(row[key]); }).reduce(function(prev, curr, index, array) { return prev && curr; })) {
                    results.meta.fields = results.meta.fields.splice(1)
                    results.data.forEach(function(row) {
                        data["dataset"].push(row[key]);
                    });
                }
                data["names"] = results.meta.fields;
                
                var values = {};
                results.meta.fields.forEach(function(field) {
                    values[field] = [];
                });

                try {
                    results.data.forEach(function(row) {
                        if ($.map(row, function(v) {return v;}).length == results.meta.fields.length) {
                            results.meta.fields.forEach(function(field) {
                                if (row[field] == "-" || 
                                    row[field] == "?") 
                                {
                                    values[field].push(NaN);
                                } else if (!isNaN(row[field])) {
                                    values[field].push(row[field]);
                                } else {
                                    throw "Unexpected character";
                                }
                            });
                        }
                    });
                    
                    data["values"] = values;
                    sessionStorage["data"] = JSON.stringify(data);
                    $("#show_file").show();
                    $('#info_file').html("Done!");
						
                    window.location = APP_CONFIG.app_url + "/file.html";
                } catch (err) {
                    var resultado = "<p style=\"color:red\";><strong>" + err + "</strong></p>";
                    $('#info_file').html("<br>"+resultado);
                    $('#formfile').trigger('reset');
                }
            }
        });
	});
	
	if ($(document).find("#file_table").length > 0) {
		show_file();
	}
});

function show_file() {
    var data = JSON.parse(sessionStorage["data"]);
    
	if (!data) {
        $("#danger").html("There is no file uploaded.").show();
    } else {
        var salida = "<thead><tr>";
        if (data.dataset.length != 0) {
            salida = salida + "<th>Dataset</th>";
        }
    
        $.each(data.names, function(index, value) {
            salida = salida + "<th>" + value + "</th>";
        });
        salida = salida + "</tr></thead><tbody>";
        
        for (var i = 0; i < data.values[data.names[0]].length; i++) {
            salida = salida + "<tr>";
            if (data.dataset.length != 0) {
                salida = salida + "<td>" + data.dataset[i] + "</td>";
            }
            $.each(data.names, function(j, name) {
                salida = salida + "<td>" + data.values[name][i] + "</td>";
            });
            salida = salida + "</tr>";
        }
        
        salida = salida + "</tbody>";
        
        $('#file_table').html(salida);
    }
}

