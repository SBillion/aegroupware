from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import redirect_to

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'^$', redirect_to, {'url': '/weblog/'}),
	(r'^portal/', include('portal.urls')),
	(r'^account/', include('account.urls')),
	(r'^planner/', include('planner.urls')),
	(r'^offers/', include('product.urls')),
	(r'^static/(?P<path>.*)$', 'django.views.static.serve',
	    {'document_root': settings.MEDIA_ROOT}),

	# Uncomment the admin/doc line below to enable admin documentation:
#	(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	(r'^admin/', include(admin.site.urls)),

	# zinnia weblog
	(r'^weblog/', include('zinnia.urls')),
	(r'^comments/', include('django.contrib.comments.urls')),

	# djangobb
	(r'^forum/', include('djangobb.urls')),
)
