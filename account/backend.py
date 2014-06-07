from agency.models import Customer
from django.contrib.auth.models import check_password

class AuthBackend:
	def authenticate(self, username=None, password=None):
		try:
			customer = Customer.objects.get(username=username)
			valid = check_password(password, customer.password)
			if valid:
				return customer
		except Customer.DoesNotExist:
			return None

	def get_user(self, user_id):
		try:
			customer = Customer.objects.get(pk=user_id)
			return customer
		except Customer.DoesNotExist:
			return None
