/**
 * Contains the handler functions for the upload file modal and data visualization
 */


$(document).ready(function() {
    
    // Event handler of uploading a file. It parses the file using papaparse
	$(document).on('click', '#upload_file', function() {
		var formData = new FormData($('#formfile')[0]);
		var fichero = $("#file").val();
                var text = $("#import_text").val();
                
                // Gets the file from the form
                if (fichero == "" && text == "") {
                    $("#danger_file").html("<strong>You must enter either a text data or an input file.</strong>");
                    $("#danger_file").show();
                } else {
                     var csvfile = ""
                    if (fichero != "") {
                        csvfile = $("#file")[0].files[0];
                    } else {
                        csvfile = text;
                    }

                    // Parses file
                    Papa.parse(csvfile, {
                        header: true,
                        dynamicTyping: true,
                        complete: function(results) {
                            try {
                                if (results.meta.fields.length < 2) throw "Too few columns";
                                var data = {};
                                data["dataset"] = [];
                                
                                // Obtains the name of the groups/algorithms
                                var key = results.meta.fields[0];
                                if (results.data.map(function(row) { return isNaN(row[key]); }).reduce(function(prev, curr, index, array) { return prev && curr; })) {
                                    results.meta.fields = results.meta.fields.splice(1);
                                    results.data.forEach(function(row) {
                                        data["dataset"].push(row[key]);
                                        delete row[key];
                                    });
                                }
                                data["names"] = results.meta.fields;
                                
                                // Obtains the values for each group
                                var values = {};
                                results.meta.fields.forEach(function(field) {
                                    values[field] = [];
                                });
                            
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
                                
                                // Stores the data in the sessionStorage as a string
                                data["values"] = values;
                                sessionStorage["data"] = JSON.stringify(data);
                                $("#show_file").show();
                                $('#info_file').html("Done!");
                                console.log(data);
                                                            
                                window.location = APP_CONFIG.app_url + "/data.html";
                            } catch (err) {
                                $("#danger_file").html("<strong>Format not valid, please read the <a href=\"#helpModal\" data-toggle=\"modal\" more-info=\"file\">expected format</a></strong>");
                                $("#danger_file").show();
                                $('#formfile').trigger('reset');
                            }
                        }
                    });
                }
	});
	
    // Event handler to show the content of the file
	if ($(document).find("#file_table").length > 0) {
		show_file();
	}
	
	// Event handler to remove the error bar when uploading files when the modal closes
	$(document).on('hide.bs.modal', '#modal_fichero', function () {
            $("#danger_file").hide();
        });
});

/**
 * Shows the content of the data upload to the application
 */
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

