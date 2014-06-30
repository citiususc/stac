/*Muestra ayuda dependiendo de donde se venga.*/
$(document).ready(function () {
    location.hash && $(location.hash + '.collapse').collapse('in');
});

/*Scroll al accordion activo.*/
$('#accordion').on('shown.bs.collapse', function () {
  
  var panel = $(this).find('.in');
  
  $('html, body').animate({
        scrollTop: panel.offset().top
  }, 400);
  
});
