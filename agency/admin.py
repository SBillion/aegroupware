from agency.models import *
from django.db import models
from django.contrib import admin
from django.contrib.admin import widgets
import datetime
from django.contrib.auth.admin import *
from django.contrib.auth.forms import *

from django.contrib.auth.models import Group, Permission


class CustomerChangeForm(UserChangeForm):

	groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(),
	  required=False,  label='Groupes de l\'utilisateur', widget=widgets.FilteredSelectMultiple(
	  'Groupes', False, attrs={'rows': '10'}))

	user_permissions = forms.ModelMultipleChoiceField(queryset=Permission.objects.all(),
	  required=False, label='Permissions de l\'utilisateur', widget=widgets.FilteredSelectMultiple(
	  'Permissions', False, attrs={'rows': '10'}))

	class Meta(UserChangeForm.Meta):
		model = Customer
		exclude = ("is_superuser","is_staff",)
		


class CustomerAdmin(admin.ModelAdmin):
	add_form = UserCreationForm
	form = CustomerChangeForm
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('username', 'password1', 'password2', 'address',)}
		),
	)
	def get_form(self, request, obj=None, **kwargs):
		"""
		Use special form during user creation
		"""
		defaults = {}
		if obj is None:
			defaults.update({
				'form': self.add_form,
				'fields': admin.util.flatten_fieldsets(self.add_fieldsets),
			})
		defaults.update(kwargs)
		return super(CustomerAdmin, self).get_form(request, obj, **defaults)


class IntervenerChangeForm(UserChangeForm):

	class Meta(UserChangeForm.Meta):
		model = Intervener
		exclude = ("groups","user_permissions","is_superuser")

class IntervenerAdmin(admin.ModelAdmin):
	add_form = UserCreationForm
	form = IntervenerChangeForm
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('username', 'password1', 'password2')}
		),
	)
	def get_form(self, request, obj=None, **kwargs):
		"""
		Use special form during user creation
		"""
		defaults = {}
		if obj is None:
			defaults.update({
				'form': self.add_form,
				'fields': admin.util.flatten_fieldsets(self.add_fieldsets),
			})
		defaults.update(kwargs)
		return super(IntervenerAdmin, self).get_form(request, obj, **defaults)


#Invoice
class InvoiceAdminForm(forms.ModelForm):
	
	def __init__(self, *args, **kwargs):
		super(InvoiceAdminForm, self).__init__(*args, **kwargs)
		rel = models.ManyToManyRel(Product, 'id')
		query = Product.objects.filter(public=True, history=False)
		if self.instance.pk:
			query |= self.instance.products.all()
		self.fields['products'] = forms.ModelMultipleChoiceField(
		  queryset=query,
		  required=False, label='Produits de la facture', widget=widgets.FilteredSelectMultiple(
		  'Produits', False, attrs={'rows': '10'}))
		self.fields['products'].widget = widgets.RelatedFieldWidgetWrapper(
			self.fields['products'].widget, rel, self.admin_site)
		
	class Meta:
		model = Invoice

class InvoiceAdmin(admin.ModelAdmin):
	form = InvoiceAdminForm
	
	def __init__(self, model, admin_site):
		self.form.admin_site = admin_site
		super(InvoiceAdmin, self).__init__(model, admin_site)
		
	def queryset(self, request):
		qs = super(InvoiceAdmin, self).queryset(request)
		if request.user.is_superuser:
			return qs
		return qs.filter(agency__staffs=request.user)


		
class VehicleAdmin(admin.ModelAdmin):
	def queryset(self, request):
		qs = super(VehicleAdmin, self).queryset(request)
		if request.user.is_superuser:
			return qs
		return qs.filter(agency__staffs=request.user)
	list_display = ('description', 'category', 'purchase_date', 'last_revision_date', Vehicle.prochaine_revision, 'agency')

# Agency
class AgencyChangeForm(forms.ModelForm):
	

	staffs = forms.ModelMultipleChoiceField(queryset=User.objects.all(),
	  required=False, label='Staffs de l\'agence', widget=widgets.FilteredSelectMultiple(
	  'Staffs', False, attrs={'rows': '10'}))
	interveners = forms.ModelMultipleChoiceField(queryset=Intervener.objects.all(),
	  required=False, label='Intervenants de l\'agence', widget=widgets.FilteredSelectMultiple(
	  'Intervenants', False, attrs={'rows': '10'}))


	class Meta:
		model = Agency
		exclude = ("customers",)

class AgencyAdmin(admin.ModelAdmin):
	form = AgencyChangeForm

	def queryset(self, request):
		qs = super(AgencyAdmin, self).queryset(request)
		if request.user.is_superuser:
			return qs
		return qs.filter(staffs=request.user)

admin.site.register(Agency, AgencyAdmin)
admin.site.register(Intervener, IntervenerAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Session_review)
