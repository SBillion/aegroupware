from django.conf.urls.defaults import *

urlpatterns = patterns('planner.views',
	(r'^source/(?P<type>.*)/(?P<id>\d+)$', 'get_events'),
	(r'^dateupdate/$', 'update_event_date'),
	(r'^addevent/$', 'add_event'),
	(r'^self_reg/$', 'self_reg'),
	(r'^user_reg/$', 'user_reg'),
	(r'^vehicles/$', 'get_vehicles'),
)
