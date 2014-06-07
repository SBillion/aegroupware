from product.models import Product
from django import forms
from django.db import models
from django.contrib import admin
from django.contrib.admin import widgets

class ProductAdminForm(forms.ModelForm):
	pack_product = forms.ModelMultipleChoiceField(queryset=Product.objects.filter(history=False),
		required=False, label='Produits du pack', widget=widgets.FilteredSelectMultiple(
		'Produits', False, attrs={'rows': '10'}))
		
	def __init__(self, *args, **kwargs):
		super(ProductAdminForm, self).__init__(*args, **kwargs)
		rel = models.ManyToManyRel(Product, 'id')
		self.fields['pack_product'].widget = widgets.RelatedFieldWidgetWrapper(
		  self.fields['pack_product'].widget, rel, self.admin_site)
		  
	class Meta:
		model = Product


class ProductAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'public', 'price', '__is_pack__')
	form = ProductAdminForm
	
	def __init__(self, model, admin_site):
		self.form.admin_site = admin_site
		super(ProductAdmin, self).__init__(model, admin_site)
	
	def queryset(self, request):
		qs = super(ProductAdmin, self).queryset(request)
		return qs.filter(history=False)

admin.site.register(Product, ProductAdmin)
