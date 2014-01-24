define(['jquery', 'check_internet_connectivity',], function($, check_connectivity) {
	var sync_button = {
    	
		//Method to highlight sync button when connectivity returns
        highlight_sync: function() {
        	var highlight_timeout = 5000;
        	
        	$('#sync').addClass('btn-success');
        	setTimeout(function(){
                $("#sync").removeClass('btn-success');
             }, highlight_timeout)
        },
        
        //Ping the server to check if user is online or offline. This is currently used when upload queue is not empty.
        ping_when_offline : function() {
        	var that = this;
        	check_connectivity.is_internet_connected()
        	.done(function(){
        		//Highlight sync button
        		that.highlight_sync();
        	})
        	.fail(function(){
        		//Do nothing
        	});
        }
    };	
    return sync_button;
});