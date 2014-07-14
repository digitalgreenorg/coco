#COCO.js for data collection
COCO.js is a library designed to help you to quickly create a single-page application (SPA) to collect data online or offline despite flaky internet connectivity. It is specially recommended for use cases with high mobility or low connectivity.
* Collect any data - specify your data through a JavaScript configuration file - config.js.
* Use on any device - responsive UI courtesy Bootstrap 3
* Capture data offline and sync when online
* Sort and search and export data to Excel - through datatables.js
* Connect with any database through a REST API

##3 steps to COCO.js
0. Copy main.js, config.js and dashboard.html from the COCO repository into your code.
1. Design your forms and put them in dashboard.html. Freely use Bootstrap, mustache/handlebars, chosen, underscore and your own JavaScript to include complex functionality.
2. Configure your application in configs.js using this documentation.
3. Create a REST API, and some COCO specific APIs over your database on your server.

## Write your configs.js file

Loosely, we configure an entity through the configs.js for each form we want to fill through COCO. To configure an entity:

	var person_configs = {
		'entity_name': 'person',
		'rest_api_url': '/coco/api/v1/person/',
		'page_header': 'Person',
		'add_template_name': 'person_add_edit_template',
		'edit_template_name': 'person_add_edit_template',
		'form_field_validation': {
		// jQuery validation for form inputs
			rules: {
        			name: {
                    		required: true,
                    		}
                	},
		 },
	};

Following is the description of above attributes:

Attribute Name             | Type        | Description
---------------------------|-------------|------------------------------------------------------------------
entity_name                | String      | Name of the object in indexed DB. It is used for accessing this object.	
rest_api_url               | String      | The REST URL for this entity
page_header                | String      | The name that needs to shown in headers (on dashboard as well as list view)
dashboard_display          | Object      | Configures how this shows up on the COCO dashboard
dashboard_display.list	   | Boolean     | Determines whether the list page is to be enabled or not.
dashboard_display.add	   | Boolean     | Determines whether add and edit is allowed or not.
dashboard_display.enable_months | Array of numbers | Index of months for which add should be enabled. (Starts from 1)
add_template_name          | String: Id of HTML template   | The id of template in dashboard.html used to add data.
edit_template_name         | String: Id of HTML template   | The id of template in dashboard.html used to edit data.
form_field_validation      | Object      | Validation check on the form.
unique_together_field      | List of strings | This combination of values is checked for uniqueness within the table. It is similar to the unique_together attribute in Django models.
foreign_entities           | Object      | Configuration of the foreign elements used by this entity.
sort_field                 | String      | When this is a foreign entity, the name of the field in the json object stored in the database on which the data is sorted.

To define foreign entities to be references within this entity, add the following object:

    foreign_entities : {
        foreign_entity_name:{ 
            attribute_name_in _json:{
            }
        }
    }

Here foreign_entity_name is the entity_name of the foreign element and attribute_name_in_json is the attribute name of this foreign element in json. The attribut_name_in_json has the following attributes:

Attribute Name| Type            | Description
--------------|-----------------|------------------------------------------------------------------------------------------
placeholder   | String          | The id of the element in form's html (in dashboard.html) where the dropdown of this foreign entity is inserted.
name_field    | String          | the attribute name in f_entity's json which needs to be shown in its dropdown	
dependency    | list            | The choices available in this foreign key are included if the value of an attribute is the same as the value selected earlier in the form.
filter        | dictionary      | whether to filter the objects of foreign entity before rendering into dropdown
id_field      | String          | The name of id field for this foreign entity in denormalised json
		
		
dependency attribute of foreign field have following attributes. Syntax:
	'dependency': [{
		'source_form_element': 'village',
		'dep_attr': 'village'
		'src_attr' : 'village'
	}],

Attribute Name      | Type   | Description
--------------------|--------|---------------------------------------------------------------------------------------------
source_form_element | String | attribute name of source element in json
dep_attr            | String | the attribute name in json of dependent foreign entity which refers to source foreign entity
src_attr            | String | to compare dep_attr of dependent element with a particular attribute in source foreign entity
		

filter attribute of foreign field have following attributes. Syntax:

'filter': {
	
		'filter': {
			attr: 'group', //the attribute name in f_entity's json to filter on
			value: null	//desired value of the attr
		},		
	
Attribute Name| Type            | Description
--------------|-----------------|-----------------------------------------------------
attr          | String          | the attribute name in f_entity's json to filter on
value         | String          | desired value of the attr
		

If separate foreign entities are needed for add and edit view, then those foreign entities can be put inside add : {} or edit : {}

There can be cases where we need an inline form or a bulk form.

### Special forms: Inline forms

If we want to include some other entity's form inline inside our current entity's form, then we use inline attribute of the entity.

Syntax:

	'inline': {
		'entity': 'person',
		'default_num_rows': 10,
		"template": "person_inline",
		"joining_attribute": {
			'host_attribute': ["id", "group_name"],
			'inline_attribute': "group"
		},
		"header": "person_inline_header",
		'borrow_attributes': [{
			'host_attribute': 'village',
			'inline_attribute': 'village'
		}],
		foreign_entities: { //used at convert_namespace, denormalize
			only village: {
				village: {
					placeholder: 'id_village', name_field: 'village_name'
				},
			},
			group: {
				group: {
					placeholder: 'id_group', name_field: 'group_name'
				}
			}
		}
	},


Attribute Name    | Type          | Description
------------------|---------------|----------------------------------------------------------------------------------------
entity            | String        | the name of the entity which needs to be inserted into current entity.
default_num_rows  | number        | number of rows to be shown by default to the user.
template          | HTML          | The  id  of  the  template  used  inside template	dashboard.html for this form.
joining_attribute | dictionary    | It denotes the attribute that joins the inline entity with the main entity.
header            | HTML Template |  
borrow_attributes | dictionary    | It denotes the attribute that the inline form's entity needs to borrow from the main entity.
		

The borrow_attributes and joining_attribute has two attributes:
1. host_attribute - The list of single attribute from the host entity. 
2. inline_attribute - The attribute corresponding to host_attribute for inline entity. 


### Special forms - bulk forms
Bulk forms are used when multiple objects of the entity can be saved through its add form. Bulk form is usually written inside add: {}
All the fields which are required inside the bulk form are added inside the braces of 'bulk':{}

Syntax:
 
	'add' : {
		'bulk': {
			foreign_fields: { //foreign fields in the individual objects 
				"video": {
					video: {
						'name_field': 'title'
					}
				},
				"person": {
					person: {
						'name_field': 'person_name'
					}
				},
				village: {
					village:{
						'name_field': 'village_name'
					}
				},
				group: {
					group:{
						'name_field': 'group_name'
					}
				}
			},
			borrow_fields: ['village', 'group']
		}
	},

If the fields in bulk form are dependent on values of fields in form, then we use borrow_fields attribute.

###Validations:
Validations can be done inside each entity using same syntax as that of jquery validation.

##How to setup COCO with a server:
1. Design your database models
2. Setup a REST api
3. Write the views required by COCO on the server-side.
4. Ensure that the dashboard.html file is rendered when the url is accessed. 
5. Ensure that the path of main.js file (in coco/dist directory) and path of configs.js are specified correctly in dashboard.html file. 

COCO communicates with the server using the following urls:

1.	**/coco/login/ :** COCO sends 'username' and 'password' parameters using POST to the URL /coco/login/ and it expects "1" as a response in case the authentication is successful otherwise it expects "0". 
2.	**/coco/logout/ :** COCO sends a POST request to the URL /coco/logout/ and on success, it logs out the user. 
3.	**/api/api_name/ :** In order to communicate with the database using RESTful service, the url for the REST API needs to be specified in the configs.js file in the parameter 'rest_api_url'. Its not compulsory to use /api/ URL, but it is recommended. 
4.	**/coco/reset_database_check/ :** This URL can be changed in configs file. COCO sends a get request to this url with a parameter 'lastdownloadtimestamp'. The server sends "1" as a response if it wants the client to download the database again. 
5.	**/coco/record_full_download_time/ :** The URL can be changed in configs file. COCO sends a post request to this URL with start_time and end_time as the parameters. These parameters are useful for recording total database download time. 
6.	**/get_log/ :** User can change this URL in configs.misc.inc_download_url. COCO sends a get request to this URL along with last_download_timestamp as a parameter. The server should send the data having timestamp later than the timestamp received from the client. 

##How to make an app on COCO (Example specific to Django)

####COCO architecture needs to you work on following things for creating your own app over it:

1. Server Side:
  1. Models in Django 
  2. REST Api using TastyPie 
2. Client Side: 
  1. Configuration javascript file (config.js) 
  2. HTML Templates using underscore templating language. 

####Following are the detailed steps for creating applications:
1. Create a Django project. Configure the database details in settings.py 
2. Copy the COCO folder in project/project_name/media folder 
3. In settings.py, make the following changes: 
  1. Set STATIC_URL = '/media/' 
  2. Set STATICFILES_DIRS = ( os.path.join(PROJECT_PATH, 'media'), ) 
  3. Set TEMPLATE_DIRS = ( os.path.join(PROJECT_PATH, 'media/coco/app') ) 
4. Create a new app and register the app in settings.py 
5. Create models in that app as per the requirement in models.py 
  1.	Create a Usermodel class which will be used for storing the user identity if there are multiple users. Later inherit this Usermodel class in all other model classes. Class Usermodel can be created as below: 

			class UserModel(models.Model):
				user_created = models.ForeignKey(User, related_name ="%(class)s_created", editable = False, null=True, blank=True)
				time_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
				user_modified = models.ForeignKey(User, related_name ="%(class)s_related_modified",editable = False, null=True, blank=True)
				time_modified = models.DateTimeField(auto_now=True, null=True, blank=True)
		
			class Meta:
				abstract = True
		
		The above class saves the timestamp for when the user was created and when its details were modified. In Tastypie it is not possible to determine both username and whether created or modified at the same place. Therefore, user_created and user_modified will be saved as null.

  2.	If you need to assign some particular village/state/area to some user then create a class CocoUser which will store this mapping:

			class CocoUser(UserModel):
				user = models.OneToOneField(User)
				states = models.ManyToManyField(State)
		
		All models which are to be selectively downloaded (example user specific) must contain the assigned field (state in above case). Create this class if there are multiple users of coco and each enters data according to different state/department etc.
 
6. After creating models, we need to create RestAPIs for performing operations on our database. For this, create a file api.py in django app and do the following: 
  1.	Create a class called baseresource which will be inherited by the resource classes which is to be shown to users i.e. the tables that could be modified by the user. We are creating this class called base resource so that we may store the id the user entering the data. The base resource class needs to have a full_hydrate function which will be used for denormalizing the JSON file that is sent to server. 

			class BaseResource(ModelResource):
				
				def full_hydrate(self, bundle):
					bundle = super(BaseResource, self).full_hydrate(bundle)
					bundle.obj.user_modified_id = bundle.request.user.id return bundle
		
				def obj _create(self, bundle, **kwargs):
					"""
					A ORM-specific implementation of ``obj_create``.
					"""
					bundle.obj = self._meta.object_class()
			
					for	key, value in kwargs.items():
						setattr(bundle.obj, key, value)
				
					self.authorized_create_detail(self.get_object_list(bundle.request), bundle)
					bundle = self.full_hydrate(bundle)
					bundle.obj.user_created_id = bundle.request.user.id return self.save(bundle)
			
  2.	Add a function dict_to_foreign_uri which generate a foreign uri for a given field in a dictionary. 
		
			def	dict_to_foreign_uri(bundle, field_name, resource_name=None):
				field_dict = bundle.data.get(field_name)
				if field_dict:
					bundle.data[field_name] = "/api/v1/%s/%s/"%(resource_name if resource_ name else field_name, str(field_dict))
				else:
					bundle.data[field_name] = None return bundle

  3.	Add a class for Authorization. The authorization can be given to a user based on some specific fields like in the following example code, we give authorization to the user based on the state assigned to him. 

			class StateLevelAuthorization(Authorization):
				def __init__(self, field):
					self.state_field = field
			
				def read_list(self, object_list, bundle):
					states = CocoUser.objects.get(user_id= bundle.request.user.id).get_state()
					kwargs = {} kwargs[self.state_field] = states
					return object_list.filter(**kwargs).distinct()
			
				def read_detail(self, object_list, bundle):
					# Is the requested object owned by the user?
					kwargs = {}
					kwargs[self.state_field] = CocoUser.objects.get(user_id= bundle.request.user.id).get_state()
					obj = object_list.filter(**kwargs).distinct()
					if obj:
						return True
					else:
						raise NotFound( "Not allowed to download" )

  4.	The authorization class created above should be used in Meta class's authorization field. 

7. Copy the media folder which contains the coco code into project/project_name folder. We now need to code two files, configs.js and dashboard.html file. 
8. Configs.js file is used for configuring the forms. Each variable defined in this file either represents a server side model or a form. The dummy_config variable in the file represents a dummy configuration and describe the use of each of the options. 
9. Dashboard.html have a list view as well as the add/edit view. The templates for these views need to be defines. The ids of these views needs to be same as that defined in configs.js. 
10. Compile the js files using grunt. Go inside coco folder and type this command: "grunt roptimize" into the command line. This action will result into generation of main.js inside /media/coco/dist/scripts folder. If there are other js libraries which needs to be included in main.js files then do the require changes in /media/coco/app/scripts/main.js as well as /media/coco/gruntfile.js 
11. Incremental download feature checks the server every 5 mins if there are updates on server which are not present on the client. These updates might have been made by some other user who is assigned same state/village/department etc. Whenever a user enters a data, server stores the timestamp of the entry along with the user as well as state/village/Department in the table serverlog. Following is the serverlog code to be written in models.py: 

		class ServerLog(models.Model):
			timestamp = models.DateTimeField(default=datetime.datetime.utcnow)
			user = models.ForeignKey(User, null = True)
			state = models.IntegerField(null = True)
			action = models.IntegerField()
			entry_table = models.CharField(max_length=100)
			model_id = models.IntegerField(null = True)

12. For maintaining the logs related to when an entry was saved/deleted or if there are any updated logs, create a file data_log.py in the app. This file handles the request related to incremental download, add/delete logs. Now we need to trigger signals whenever a save/delete event occurs. For this, write these two lines after every class which saves the data that is entered by the user:

		post_save.connect(save_log, sender = Progress)
		pre_delete.connect(delete_log, sender = Progress)

	The sender's value here should be equal to name of the class. save_log and delete_log can be imported from django.db.models.signals

13. For storing the info regarding the database downloads made by the user, write the following code in models.py

		class FullDownloadStats(models.Model):
			user = models.ForeignKey(User)
			start_time = models.DateTimeField()
			end_time = models.DateTimeField()
		
