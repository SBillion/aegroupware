# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User, Group
from django.dispatch import dispatcher
from product.models import Product
from django.db.models.signals import m2m_changed, pre_save, post_save
from SessionManager import createSession
from signals import *
from dateutil.relativedelta import relativedelta

import datetime
import time

class Customer(User):
	address = models.CharField(max_length=255, blank=True)
#	invoices from Agency.Invoice
#	events from Planner.Event
#	agencies from Agency.Agency

	def reg_at_event(self, event):
		from portal.models import Session
		duration = relativedelta(event.end, event.start).hours
		try:
			try:
				prod = Product.objects.filter(type = event.type)
			except Product.DoesNotExist:
				return False
			session_reviews = Session_review.objects.filter(product = prod)
		except Session_review.DoesNotExist:
			return False
		available_time = 0;
		for session_review in session_reviews:
			available_time += (session_review.product.hours - session_review.spent_hours)
		if available_time >= duration:
			for session_review in session_reviews:
				sess_available_time = session_review.product.hours - session_review.spent_hours
				if sess_available_time >= duration:
					session_review.spent_hours += duration
					session_review.save()
					break
				elif sess_available_time > 0:
					session_review.spent_hours += sess_available_time
					duration -= sess_available_time
					session_review.save()
			session = Session(customer = self, event = event)
			session.save()
			return True
		else:
			return False

	def __unicode__(self):
		return 'Customer %s au %s' % (self.username, self.address)

class Intervener(User):
	def __unicode__(self):
		if self.last_name and self.first_name:
			return '%s %s' % (self.last_name,self.first_name)
		else:
			return self.username
	def save(self):
		self.is_staff = True
		super(Intervener, self).save()
		
	post_save.connect(add_group_to_intervener)

class Agency(models.Model):
	name = models.CharField(max_length=255)
	address = models.CharField(max_length=255)
	customers = models.ManyToManyField('customer', null=True, blank=True, related_name='agencies')
	staffs = models.ManyToManyField(User)
	interveners = models.ManyToManyField('intervener',null=True,blank=True,related_name='agencies')
#	invoices from Agency.Invoice
#	vehicles from Agency.Vehicle
#	events from Planner.Event

	def __unicode__(self):
		return 'Agence %s au %s' % (self.name, self.address)


CATEGORY_VEHICLE = (
	(1, 'auto'),
	(2, 'moto'),
)

class Vehicle(models.Model):
	description = models.CharField(max_length=255)
	category = models.SmallIntegerField(max_length=1, choices=CATEGORY_VEHICLE)
	purchase_date = models.DateField()
	last_revision_date = models.DateField(blank=True, null=True)
	agency = models.ForeignKey(Agency, related_name='vehicles')
	extra = models.TextField(blank=True)
#	events from Planner.Event

	def prochaine_revision(self):
		if self.last_revision_date:
			date_plus_3_months = self.last_revision_date + datetime.timedelta(days=3*30)
		else:
			date_plus_3_months = self.purchase_date + datetime.timedelta(days=3*30)
		return date_plus_3_months

	def next_revision_period(self):
		t = datetime.time(0, 0, 0, 0)
		rev = datetime.datetime.combine(self.prochaine_revision(), t)
		end_rev = datetime.datetime.combine(rev + datetime.timedelta(days=7), t)

		return (rev, end_rev)

	def is_available(self, start, end):
		(rev, end_rev) = self.next_revision_period()
		if rev < start < end_rev or rev < end < end_rev:
			return False
		events = self.events.all()
		for event in events:
			if event.start <= start and event.end > start:
				return False
			elif event.start >= start and event.start < end:
				return False
			elif event.start >= start and event.end <= end:
				return False
		return True

	def __unicode__(self):
		return u'Véhicule %s de l\'agence: %s' % (self.description, self.agency)


CATEGORY_INVOICE = (
	(1, 'complete'),
	(2, 'pending'),
)



class Invoice(models.Model):
	date = models.DateTimeField(auto_now_add=True)
	price = models.FloatField()
	#articles = models.CharField(max_length=256000)
	products = models.ManyToManyField(Product, symmetrical=False, related_name='invoices')
	status = models.SmallIntegerField(max_length=1, choices=CATEGORY_INVOICE)
	customer = models.ForeignKey(Customer,  related_name='invoices')
	agency = models.ForeignKey(Agency, related_name='invoices')

	def __unicode__(self):
		return 'Facture du %s de l\'utilisateur %s' % (self.date, self.customer)
	
	m2m_changed.connect(createSession)
	post_save.connect(link_customer_to_agencie)


class Session_review(models.Model):
	product = models.ForeignKey(Product, related_name='session_review')
	customer = models.ForeignKey(Customer, related_name='session_review')
	invoice = models.ForeignKey(Invoice, related_name='session_review')
	spent_hours = models.IntegerField()

	def __unicode__(self):
		return 'Customer '+self.customer.username+\
			' spent '+str(self.spent_hours)+' hours on product '+self.product.designation

