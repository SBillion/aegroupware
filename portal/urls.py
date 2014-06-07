from django.conf.urls.defaults import *

urlpatterns = patterns('portal.views',
	(r'^progress/$', 'progress_display'),
	(r'^planner/$', 'planner_display'),
)
