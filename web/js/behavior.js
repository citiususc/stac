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
		$("#warning").html("There is no file uploaded with the data needed to do the test. Please upload one before applying any test.");
		$("#warning").show();
		$('button').prop('disabled', true);
	}
    
    post_hoc_labels = $(document).find("input[type=radio][name=post_hoc]").parent()
    post_hoc_labels.on('click', function() {
        post_hoc_labels.removeClass('active');
        $(this).button('toggle');
    });
});



