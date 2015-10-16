/**
 * Contains the layout loading process
 */

$(function(){
	$.get('header.html', function(content) {
		$("head").append(content);
		$('#topbar').load('topbar.html');
		$('#modals').load('modals.html');
	})
});
