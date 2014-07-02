define([
        'jquery',    
        'collections/upload_collection',
], function($, upload_collection) {
	var uploadqueue_status = {
			is_uploadqueue_empty: function() {
	            console.log("FORMCONTROLLER: length of upload_collection - " + upload_collection.length);
	            console.log(upload_collection);

	            return upload_collection.fetched && upload_collection.length <= 0;
	        },
    };	
    return uploadqueue_status;
});