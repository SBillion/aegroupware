#Add intervener at group intervenants Agency when intervener account is create
def add_group_to_intervener(sender,  **kwargs ):
	from django.contrib.auth.models import Group
	from models import Intervener
	obj = kwargs['instance']
	if isinstance(obj, Intervener):

		intervener = Intervener.objects.get(id=obj.id)
		g = Group.objects.get(name='Intervenants Agence')
		intervener.groups.add(g)


#Link a customer to an agencie when a facture for this customer is create
def link_customer_to_agencie(sender, **kwargs):
	from models import Invoice
	obj = kwargs['instance']
	if isinstance(obj, Invoice):
		invoice = Invoice.objects.get(id=obj.id)
		customer = invoice.customer
		agency = invoice.agency
		agency.customers.add(customer)
		agency.save()
