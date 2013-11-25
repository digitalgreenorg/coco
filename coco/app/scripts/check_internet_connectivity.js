define(['jquery'], function($) {
	var check_connectivity={
			is_internet_connected : function(){
				return $.get("/coco/check_connectivity/");
	        },
	}
	return check_connectivity;
});