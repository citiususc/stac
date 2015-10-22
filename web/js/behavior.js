/**
 * Contains the handler functions for the whole page
 */

$(document).ready(function(){
	// Expands info on the help modal
	$(document).on('click', 'a[more-info]', function() {
		var id = "#"+$(this).attr('more-info')+"_info"
		if (!$(id).hasClass('in')) {
			$("#accordion a[data-toggle=collapse][href='"+id+"']").click();
		}
	});
	
    // Check if data was already loaded
	if (!sessionStorage.getItem("data")) {
		$("#warning").html("There is no file uploaded with the data needed to do the test. Please <a href=\"#modal_fichero\" data-toggle=\"modal\">upload</a> one before applying any test.");
		$("#warning").show();
		$('#apply').prop('disabled', true);
	} else {
        names = JSON.parse(sessionStorage.data).names
        // Controls the content of groups to be selected for two group tests
        if ($("#group1").length) {
            names.forEach(function(name) {
                $("#group1").append("<option value=\""+name+"\">"+name+"</option>");
                $("#group2").append("<option value=\""+name+"\">"+name+"</option>");
            });
            if ($("#group2 option").length > 1) {
                $($("#group2 option")[1]).prop('selected', true);
            }
        }
        // Controls the content of control method combobox
        if ($("#control").length) {
            names.forEach(function(name) {
                $("#control").append("<option value=\""+name+"\">"+name+"</option>");
            });
        }
    }
    
    // Controls the active class in the list of post-hoc methods
    post_hoc_labels = $(document).find("input[type=radio][name=post_hoc]").parent()
    post_hoc_labels.on('click', function() {
        post_hoc_labels.removeClass('active');
        $(this).button('toggle');
    });
    
    // Event handler that shows the content to be exported when activating the modal
    $(document).on('change', '.btn-file :file', function() {
        var input = $(this),
            numFiles = input.get(0).files ? input.get(0).files.length : 1,
            label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
            $(this).parents('.input-group').find(':text').val(label);
    });
    
});



