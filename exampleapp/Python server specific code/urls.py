from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from tastypie.api import Api

from views import exampleapp, debug, login, logout
from api import VillageResource, GroupResource, PersonResource, UserResource

v1_api = Api(api_name='v1')
v1_api.register(VillageResource())
v1_api.register(GroupResource())
v1_api.register(PersonResource())
v1_api.register(UserResource())
urlpatterns = patterns('',
    (r'^api/', include(v1_api.urls)),
    (r'^login/', login),
    (r'^logout/', logout),
    (r'^debug/', debug),
    (r'^$', exampleapp),
)