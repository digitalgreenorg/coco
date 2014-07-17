# whats missing
* quick and dirty coco app
* how to write configs
* how to write dashboard.html 
* how to create REST API
* urls
* views
* models


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

### Designing forms in dashboard.html
1. In dashboard.html, there is some code written, you have to append your form templates at the end of this file.
2. Start by writing a simple form to add person data

	```
	<script type="text/template" id="example_village_add_edit_template">
	        <fieldset class="form-horizontal">
	            
	            <legend>Add Village</legend>

	            <p class="bold-helptext"> All fields in bold are required</p>
	            
	            <div class="form-group"> 
	                <label class="control-label col-sm-2">Name</label>
	                <div class="col-sm-4">
	                    <input type="text" name="name" class="form-control">
	                </div>
	            </div>

	            <div class="form-group"> 
	                <label class="control-label col-sm-2">District Name</label>
	                <div class="col-sm-4"> 
	                    <input type="text" name="district_name" class="form-control">
	                </div>
	            </div>

	            <div class="form-group"> 
	                <label class="control-label col-sm-2">State Name</label>
	                <div class="col-sm-4"> 
	                    <input type="text" name="state_name" class="form-control">
	                </div>
	            </div>    
	        </fieldset>
	</script>
	```
  1. COCO uses underscore templating language, hence the first script tag is compulsory. The 'id' is used in the configs file to reference this form template
  2. Inside the fieldset tag, you can structure your fonts the way you like
  3. In the Input tags, name field is used to refer in the configs file.

### Writing configs for this form
1. Configs is used to connect our HTML Form to the framework. This is done by writing entities in the configs file. Loosely, entities are defined for any form we want to fill in the framework.
2. Configs basically returns an object of entities. A miscellaneous entity is required from the framework. We recommend you not to change that unless you are sure about what you are doing.
3. Start by writing a simple entity

```
	var example_village_configs = {
        'page_header': 'Village',
        'add_template_name': 'example_village_add_edit_template',
        'edit_template_name': 'example_village_add_edit_template',
        'rest_api_url': '/exampleapp/api/v1/village/',
        'entity_name': 'examplevillage',
        'dashboard_display': {
            listing: true,
            add: true
        },
        'sort_field': 'name'
    };

    return {
        example_village: example_village_configs,
        misc : misc
    }
```

  1. 'add_template_name' and 'edit_template_name' are the id's of the form that we defined in the dashboard.html
  2. 'rest_api_url' is used to fetch data from the server and to add/edit the data.
  3. 'dashboard_display' configures whether we can view the data or we can add/edit it or both

And *You're DONE!* You have successfully configured your COCO app to add and edit village information. 
Just keep adding forms in dashboard.html and entities in configs, and build your system.

This ofcourse depends upon the REST API used to store information. For a python specific example please checkout the example app and the tutorial.

#### Help us in our endevour to continuosly update the COCO library. Feel Free to fork our code or SEND PULL REQUESTS.
