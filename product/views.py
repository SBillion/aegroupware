from django.shortcuts import render_to_response
from django.template import RequestContext
from product.models import Product

def list_products(request):
    products = Product.objects.filter(public=True, history=False)
    return render_to_response('product/list_products.html',{"products": products} , context_instance=RequestContext(request))
