from django.conf.urls.defaults import *

urlpatterns = patterns('account.views',
	(r'^login/$', 'login'),
	(r'^logout/$', 'logout'),
	(r'^register/$', 'register'),
)
