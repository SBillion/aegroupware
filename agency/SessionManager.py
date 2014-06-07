from django.db import models
from django.contrib.auth.models import Group


def createSession(sender, **kwargs):
	from agency.models import Invoice
	from agency.models import Session_review
	# XXX remove this
	#for key in kwargs:
	#	print str(key)+' => '+str(kwargs[key])
	obj = kwargs['instance']
	if isinstance(obj, Invoice):
		invoice = Invoice.objects.get(id=obj.id)
		for product in invoice.products.all():
			# XXX recursively check sub product in case of pack
			if not product.history:
				session = None
			try:
				session = Session_review.objects.get(product=product, customer=invoice.customer,
				  invoice=invoice)
			except Session_review.DoesNotExist:
				session = Session_review(product=product, spent_hours=0, customer=invoice.customer,
				  invoice=invoice)
				session.save()
