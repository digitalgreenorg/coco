define([
  'jquery',
  'backbone',
  'indexeddb_backbone_config',
  'indexeddb-backbone',
  'collections/upload_collection',
  'check_internet_connectivity'
  // Using the Require.js text! plugin, we are loaded raw text
  // which will be used as our views primary template
  // 'text!templates/project/list.html'
], function(jquery, backbone, indexeddb, idb_backbone_adapter, UploadCollection, check_connectivity){
    
    var generic_model_offline = Backbone.Model.extend({
        database: indexeddb,
        storeName: "user",
        // This function is never used
//        isOnline: function(){
//        	return check_connectivity.is_internet_connected();
//        },
        isLoggedIn: function(){
            //TODO: should fetch itself first to get latest state?
            // should this be handled by the auth module
            return this.get("loggedin");
        },
        // This function is never used
//        canSaveOnline: function(){
//            return this.isOnline() && UploadCollection.fetched && UploadCollection.length===0;
//        }
    });
    var user_model = new generic_model_offline();
    user_model.set({key: "user_info"});
    
  return user_model;
});