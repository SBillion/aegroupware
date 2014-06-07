# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from portal.models import Session
from planner.models import Event
from planner.models import EVENT_TYPE
from agency.models import Customer
from agency.models import Vehicle
from agency.models import Agency

import calendar
import simplejson
from datetime import datetime
import time

def get_type_str(temp_typ):
	for typ in EVENT_TYPE:
		try:
			index = typ.index(temp_typ)
			if index != None:
				ev_type = temp_typ
				type_str = typ[1]
				return (ev_type, type_str)
		except:
			pass

@login_required
def get_vehicles(request):
	if request.method == 'GET':
		if 'application/json' in request.META.get('HTTP_ACCEPT', ''):
			if 'start_time' in request.GET and 'end_time' in request.GET:
				start = datetime(*time.gmtime(float(request.GET['start_time'])/1000)[:6])
				end = datetime(*time.gmtime(float(request.GET['end_time'])/1000)[:6])
				vehicles = Vehicle.objects.all()
				data = {
					'vehicles': []
				}
				for vehicle in vehicles:
					if vehicle.is_available(start, end):
						dic = {
							'id': vehicle.id,
							'description': vehicle.description,
						}
						data['vehicles'].append(dic)
				if data == []:
					dic = {
						'error': int(True),
						'msg_error': 'Aucunes voitures disponible',
					}
					data = dic
				return HttpResponse(simplejson.dumps(data), mimetype='application/json')

def can_add_event(event):
	error = False
	msg = ''
	if event.start.hour < 7:
		error = True
		msg = 'Horaire de début invalide'
	if event.end.hour > 16:
		error = True
		msg = 'Horaire de fin invalide'
	vehicles = Vehicle.objects.all()
	nb_disp = 0
	for vehicle in vehicles:
		if vehicle.is_available(event.start, event.end):
			nb_disp = nb_disp + 1
	if str(event.type) != 'code' and  str(event.type) != 'code_exam' and int(event.slots) > nb_disp:
		error = True
		msg = 'Nombre de places supérieur au nombre de véhicules disponibles(' + str(nb_disp) + ')'
	return (error, msg)

@login_required
def get_events(request, type, id):
	if request.method == 'GET':
		if 'application/json' in request.META.get('HTTP_ACCEPT', ''):
			data = []
			if str(type) == 'user':
				try:
					sessions = Session.objects.filter(customer=Customer.objects.get(id=id))
					for session in sessions:
						(ev_type, type_str) = get_type_str(str(session.event.type))
						dic = {
							'id': session.event.id,
							'title': type_str,
							'type': ev_type,
							'type_str': type_str,
							'slots_max': session.event.slots,
							'slots_available': int(session.event.slots - Session.objects.filter(event = session.event).count()),
							'start': calendar.timegm(session.event.start.timetuple()),
							'end': calendar.timegm(session.event.end.timetuple()),
							'allDay': False
						}
						data.append(dic)
				except Session.DoesNotExist:
					return None
			else:
				if str(type) == 'all':
					try:
						events=Event.objects.all()
					except Event.DoesNotExist:
						return None
				else:
					try:
						events=Event.objects.filter(type=str(type))
					except Event.DoesNotExist:
						return None
				for event in events:
					(ev_type, type_str) = get_type_str(str(event.type))
					dic = {
						'id': event.id,
						'title': type_str,
						'type': ev_type,
						'type_str': type_str,
						'slots_max': event.slots,
						'slots_available': int(event.slots - Session.objects.filter(event = event).count()),
						'start': calendar.timegm(event.start.timetuple()),
						'end': calendar.timegm(event.end.timetuple()),
						'allDay': False
					}
					data.append(dic)
			return HttpResponse(simplejson.dumps(data),
				   mimetype='application/json')
		else:
			print 'HTTP_ACCEPT json attendu'
	else:
		print 'GET attendu'

@login_required
def update_event_date(request):
	if request.method == 'POST':
		if 'application/json' in request.META.get('HTTP_ACCEPT', ''):
			if 'event_id' in request.POST and 'start' in request.POST and 'end' in request.POST:
				event_id = request.POST['event_id']
				start = request.POST['start']
				end = request.POST['end']
				try:
					temp_start = int(start)/1000
					temp_start = datetime(*time.gmtime(temp_start)[:6])
					temp_end = int(end)/1000
					temp_end = datetime(*time.gmtime(temp_end)[:6])
					event = Event.objects.get(id = event_id)
					event.start = temp_start
					event.end = temp_end
					(error, msg) = can_add_event(event)
					if not error:
						event.save()
					dic = {
						'error': int(error),
						'msg_error': msg,
					}
					return HttpResponse(simplejson.dumps(dic),
						mimetype='application/json')
				except Event.DoesNotExist:
					dic = {
						'error': int(False),
						'msg_error': 'Id non valide',
					}
					return HttpResponse(simplejson.dumps(dic),
						mimetype='application/json')

@login_required
def add_event(request):
	if request.method == 'POST':
		if 'application/json' in request.META.get('HTTP_ACCEPT', ''):
			if 'start' in request.POST and 'end' in request.POST and \
			   'slots' in request.POST and 'type' in request.POST:
				start = request.POST['start']
				end = request.POST['end']
				slots = request.POST['slots']
				typ = request.POST['type']
				vehicles = None
				if 'vehicles' in request.POST:
					vehicles = request.POST['vehicles']
				try:
					temp_start = int(start)/1000
					temp_start = datetime(*time.gmtime(temp_start)[:6])
					temp_end = int(end)/1000
					temp_end = datetime(*time.gmtime(temp_end)[:6])
					event = Event(start = temp_start, end = temp_end,
					   slots = slots, type = typ,
					   agency = Agency.objects.get(pk=1),
					   supervisor = request.user)
					(error, msg) = can_add_event(event)
					if not error:
						event.save()
						vehicles = [1, 2]
						if vehicles:
							for vehicle in vehicles:
								event.vehicle.add(vehicle)
							event.save()
					dic = {
						'error': int(error),
						'error_msg': msg,
					}
					return HttpResponse(simplejson.dumps(dic),
						mimetype='application/json')
				except Event.DoesNotExist:
					dic = {
						'error': int(True),
						'error_msg': 'Id non valide',
					}
					return HttpResponse(simplejson.dumps(dic),
						mimetype='application/json')

@login_required
def self_reg(request):
	if request.method == 'POST':
		if 'application/json' in request.META.get('HTTP_ACCEPT', ''):
			if 'event_id' in request.POST:
				event_id = request.POST['event_id']
				event = Event.objects.get(pk=event_id)
				if (event.slots - Session.objects.filter(event = event).count()) > 0:
					customer = request.user.customer
					if customer.reg_at_event(event) :
						dic = {
							'error': int(False),
							'error_msg': '',
						}
					else:
						msg = "Vous n\'avez plus assez d\'heures" + \
						   " disponibles pour vous inscrire à cet" + \
						   " évènement"
						dic = {
							'error': int(True),
							'error_msg': msg,
						}
					return HttpResponse(simplejson.dumps(dic),
						mimetype='application/json')
				else:
					msg = "Il n\'y a plus de places disponible pour" + \
					   " cet évènement"
					dic = {
							'error': int(True),
							'error_msg': msg,
						}
					return HttpResponse(simplejson.dumps(dic),
						mimetype='application/json')

@login_required
def user_reg(request):
	if request.method == 'POST':
		if 'application/json' in request.META.get('HTTP_ACCEPT', ''):
			if 'event_id' in request.POST and 'user_id' in request.POST:
				event_id = request.POST['event_id']
				customer_id = request.POST['user_id']
				event = Event.objects.get(pk=event_id)
				customer = Customer.objects.get(pk=customer_id)
				if (event.slots - Session.objects.filter(event = event).count()) > 0:
					if customer.reg_at_event(event) :
						dic = {
							'error': int(False),
							'error_msg': '',
						}
					else:
						msg = "Le client n'a plus assez d\'heures" + \
						   " disponibles pour être inscrit à cet" + \
						   " événement"
						dic = {
							'error': int(True),
							'error_msg': msg,
						}
					return HttpResponse(simplejson.dumps(dic),
						mimetype='application/json')
				else:
					msg = "Il n\'y a plus de places disponible pour" + \
					   " cet évènement"
					dic = {
							'error': int(True),
							'error_msg': msg,
						}
					return HttpResponse(simplejson.dumps(dic),
						mimetype='application/json')
