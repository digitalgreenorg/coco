define(['jquery'], function($) {
	var sync_button = {
		//Method to highlight sync button when connectivity returns
        highlight_sync: function() {
        	var highlight_timeout = 5000;
        	
        	$('#sync').addClass('btn-success');
        	setTimeout(function(){
                $("#sync").removeClass('btn-success');
             }, highlight_timeout)
        },        
    };	
    return sync_button;
});