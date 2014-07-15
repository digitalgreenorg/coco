from django.db import models
from django.contrib.auth.models import User
import datetime
from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized

# Create your models here.

from geographies.models import Village
from people.models import Person
# from programs.models import Partner


class UserModel(models.Model):
	user_created = models.ForeignKey(User, related_name="%(class)s_created", editable = False, null=True, blank=True) 
	time_created = models.DateTimeField(auto_now_add=True, null=True,blank=True)
	user_modified = models.ForeignKey(User, related_name="%(class)s_related_modified",editable = False, null=True, blank=True) 
	time_modified = models.DateTimeField(auto_now=True, null=True,blank=True) 
	class Meta:
		abstract = True


class ExampleVillage(UserModel):
    id=models.AutoField(primary_key=True, db_column='id')
    name = models.CharField(max_length=20)
    block_name = models.CharField(max_length=20)
    district_name = models.CharField(max_length=20)
    state_name = models.CharField(max_length=20)
    
class ExampleGroup(models.Model):
    id=models.AutoField(primary_key=True, db_column='id')
    name = models.CharField(max_length=20)
    village = models.ForeignKey(ExampleVillage)

class ExamplePerson(UserModel):
    id=models.AutoField(primary_key=True, db_column='id')
    name = models.CharField(max_length=20)
    village = models.ForeignKey(ExampleVillage)
    group = models.ForeignKey(ExampleGroup)

class ExampleModel(models.Model):
    user_created = models.ForeignKey(User, related_name ="%(app_label)s_%(class)s_created", editable = False, null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_modified = models.ForeignKey(User, related_name ="%(app_label)s_%(class)s_related_modified",editable = False, null=True, blank=True)
    time_modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True


class ExampleUser(ExampleModel):
    id = models.AutoField(primary_key=True)
    # old_coco_id = models.IntegerField(editable=False, null=True)
    user = models.OneToOneField(User, related_name="exampleapp_user")
    # partner = models.ForeignKey(Partner)
    villages = models.ManyToManyField(ExampleVillage)

    def get_villages(self):
        return self.villages.id

class FullDownloadStats(models.Model):
    user = models.ForeignKey(ExampleUser)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()


class ServerLog(models.Model):
	id = models.AutoField(primary_key=True)
	timestamp = models.DateTimeField(default=datetime.datetime.utcnow)
	user = models.ForeignKey(ExampleUser, related_name="serverlog_user", null=True)
	village = models.IntegerField(null=True)
	action = models.IntegerField()
	entry_table = models.CharField(max_length=100)
	model_id = models.IntegerField(null=True)