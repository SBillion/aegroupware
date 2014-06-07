# -*-coding:utf-8 -*
from django.db import models
from product_enum import PRODUCT_TYPES, PRODUCT_CATEGORIES

class Product(models.Model):
	designation = models.CharField(max_length=255)
	desc_url = models.CharField(max_length=255, null=True, blank=True)
	price = models.IntegerField(null=True, blank=True)
	public = models.BooleanField()
	history = models.BooleanField()
	type = models.CharField(max_length=50, null=True, blank=True, choices=PRODUCT_TYPES)
	hours = models.IntegerField(null=True, blank=True)
	category = models.CharField(max_length=50, null=True, blank=True, choices=PRODUCT_CATEGORIES)
	pack_product = models.ManyToManyField('self', null=True, blank=True, symmetrical=False)

	def __unicode__(self):
		if not self.price:
			return 'Produit %s au prix de %s' % (self.designation, self.price)
		return 'Produit %s au prix de %s' % (self.designation, self.price)
	
	def __is_pack__(self):
		if self.pack_product.all():
			return True
		return False
	
	def save(self):
		"""
		The object need to be save before any relation of type
		ManyToMany can be used. We have to save the object twice
		to tricks that.
		"""
		if not self.id:
			super(Product, self).save()
		else:
			other = Product(designation=self.designation, desc_url=self.desc_url, price=self.price,
				public=self.public, type=self.type, hours=self.hours, category=self.category)
			
			print 'other.id = '+ str(other.id)
			
			super(Product, other).save()
			
			print 'other.id = ' + str(other.id)
			
			other.pack_product = self.pack_product.all()
			
			try:
				current = Product.objects.get(id=self.pk)
				current.public = False
				current.history = True
				super(Product, current).save()
			except Exception:
				pass
			
			super(Product, other).save()
