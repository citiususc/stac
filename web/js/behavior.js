$(document).ready(function(){
	
	$(document).on('click', 'a[more-info]', function() {
		var id = "#"+$(this).attr('more-info')+"_info"
		if (!$(id).hasClass('in')) {
			$("#accordion a[data-toggle=collapse][href='"+id+"']").click();
		}
	});
	
	$(document).on('change', '.btn-file :file', function() {
		var input = $(this),
		  numFiles = input.get(0).files ? input.get(0).files.length : 1,
		  label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
		input.trigger('fileselect', [numFiles, label]);
	});

	$(document).on('fileselect', '.btn-file :file', function(event, numFiles, label) {
		var input = $(this).parents('.input-group').find(':text'),
			log = numFiles > 1 ? numFiles + ' files selected' : label;
		
		if( input.length ) {
			input.val(log);
		}
	});
	
	if (!sessionStorage.getItem("data")) {
		$("#warning").html("There is no file uploaded with the data needed to do the test. Please <a href=\"#modal_fichero\" data-toggle=\"modal\">upload</a> one before applying any test.");
		$("#warning").show();
		$('#apply').prop('disabled', true);
	} else {
        names = JSON.parse(sessionStorage.data).names
        if ($("#group1").length) {
            names.forEach(function(name) {
                $("#group1").append("<option value=\""+name+"\">"+name+"</option>");
                $("#group2").append("<option value=\""+name+"\">"+name+"</option>");
            });
            if ($("#group2 option").length > 1) {
                $($("#group2 option")[1]).prop('selected', true);
            }
        }
        if ($("#control").length) {
            names.forEach(function(name) {
                $("#control").append("<option value=\""+name+"\">"+name+"</option>");
            });
        }
    }
    
    
    
    post_hoc_labels = $(document).find("input[type=radio][name=post_hoc]").parent()
    post_hoc_labels.on('click', function() {
        post_hoc_labels.removeClass('active');
        $(this).button('toggle');
    });
    
    
    $(document).on('#modal_export show.bs.modal', function (e) {
        var format = $("#export_format").val();
        if (format == "latex") {
            $("#export_text").val(exportTableToLaTeX($('table')));
        } else {
            $("#export_text").val(exportTableToCSV($('table')));
        }
    });
    
    $(document).on('change', '#export_format', function (e) {
        var format = $("#export_format").val();
        if (format == "latex") {
            $("#export_text").val(exportTableToLaTeX($('table')));
        } else {
            $("#export_text").val(exportTableToCSV($('table')));
        }
    });
});



