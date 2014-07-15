from functools import partial
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict, ModelChoiceField
from tastypie import fields
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import Authorization
from tastypie.exceptions import NotFound
from tastypie.resources import ModelResource, NOT_AVAILABLE
from tastypie.validation import FormValidation

from exampleapp.models import ExampleVillage, ExampleGroup, ExamplePerson, ExampleUser


class BaseResource(ModelResource): 
	 
	def full_hydrate(self, bundle): 
		bundle = super(BaseResource, self).full_hydrate(bundle) 
		bundle.obj.user_modified_id = bundle.request.user.id 
		return bundle 
	 
	def obj_create(self, bundle, **kwargs): 
		""" 
		A ORM-specific implementation of ``obj_create``. 
		""" 
		bundle.obj = self._meta.object_class() 

		for key, value in kwargs.items(): 
			setattr(bundle.obj, key, value)
		 
		self.authorized_create_detail(self.get_object_list(bundle.request), bundle) 
		bundle = self.full_hydrate(bundle)
		bundle.obj.user_created_id = bundle.request.user.id
		return self.save(bundle)

	def dict_to_foreign_uri(bundle, field_name, resource_name=None): 
		field_dict = bundle.data.get(field_name) 
		if field_dict: 
			bundle.data[field_name] = "/api/v1/%s/%s/"%(resource_name if resource_name else field_name, str(field_dict)) 
		else: 
			bundle.data[field_name] = None
		return bundle


class VillageLevelAuthorization(Authorization): 
	def __init__(self, field): 
		self.villages = field

	def read_list(self, object_list, bundle): 
		states = CocoUser.objects.get(user_id= bundle.request.user.id).get_villages() 
		kwargs = {} 
		kwargs[self.villages] = states 
		return object_list.filter(**kwargs).distinct() 
 
	def read_detail(self, object_list, bundle):
		# Is the requested object owned by the user? 
		kwargs = {} 
		kwargs[self.villages] = CocoUser.objects.get(user_id= bundle.request.user.id).get_villages() 
		obj = object_list.filter(**kwargs).distinct() 
		if obj: 
			return True 
		else: 
			raise NotFound( "Not allowed to download" )

def foreign_key_to_id(bundle, field_name,sub_field_names):
	field = getattr(bundle.obj, field_name)
	if(field == None):
		dict = {}
		for sub_field in sub_field_names:
			dict[sub_field] = None 
	else:
		dict = model_to_dict(field, fields=sub_field_names, exclude=[])
	return dict

class VillageResource(BaseResource):

	# nandini: add the fields which have been chosen. so that if we want a field to come through the api we have to add it here.
	class Meta:
		authentication = SessionAuthentication()
		always_return_data = True
		queryset = ExampleVillage.objects.all()
		authorization = Authorization()

class GroupResource(BaseResource):
	village = fields.ForeignKey('exampleapp.api.VillageResource', 'village')
	# nandini: add the fields which have been chosen. so that if we want a field to come through the api we have to add it here.
	dehydrate_village = partial(foreign_key_to_id, field_name='village',sub_field_names=['id','name'])
	class Meta:
		authentication = SessionAuthentication()
		always_return_data = True
		queryset = ExampleGroup.objects.all()
		authorization = Authorization()
	

class PersonResource(BaseResource):
	village = fields.ForeignKey('exampleapp.api.VillageResource', 'village')
	group = fields.ForeignKey('exampleapp.api.GroupResource', 'group')
	# nandini: add the fields which have been chosen. so that if we want a field to come through the api we have to add it here.
	class Meta:
		authentication = SessionAuthentication()
		always_return_data = True
		queryset = ExamplePerson.objects.all()
		authorization = Authorization()
	dehydrate_village = partial(foreign_key_to_id, field_name='village',sub_field_names=['id','name'])
	dehydrate_group = partial(foreign_key_to_id, field_name='group',sub_field_names=['id','name'])


class UserResource(BaseResource):

	# nandini: add the fields which have been chosen. so that if we want a field to come through the api we have to add it here.
	class Meta:
		authentication = SessionAuthentication()
		always_return_data = True
		queryset = ExampleUser.objects.all()
		authorization = Authorization()