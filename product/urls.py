from django.conf.urls.defaults import *

urlpatterns = patterns('product.views',
	(r'^$', 'list_products'),
)
