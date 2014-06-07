from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from agency.models import Customer
from planner.models import EVENT_TYPE
from product.product_enum import PRODUCT_DEFAULT_LIMITS

import calendar
import simplejson as json
from datetime import datetime
import time

from models import *

@login_required
def progress_display(request):
	sessions = Session.objects.filter(customer=request.user)
	data = []
	if sessions:
		for session in sessions:
			try:
				data.append([calendar.timegm(session.event.start.timetuple()) * 1000,
					int(session.mark)])
			except:
				pass
	return render_to_response('portal/progress_monitoring.html',
	    { "sessions": sessions, "data": data }, context_instance=RequestContext(request))


@login_required
def planner_display(request):
	customers = Customer.objects.all()
	rights = {
		'add_event': int(request.user.has_perm('planner.add_event')),
		'change_event': int(request.user.has_perm('planner.change_event')),
		'delete_event': int(request.user.has_perm('planner.delete_event')),
	}
	default_limits = {}
	for default_limit in PRODUCT_DEFAULT_LIMITS:
		default_limits[default_limit[0]] = default_limit[1]
	return render_to_response('portal/planner.html', {"rights": rights, "event_types": EVENT_TYPE, "default_limits": default_limits, "customers": customers}, context_instance=RequestContext(request))
