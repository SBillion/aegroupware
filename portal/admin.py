from portal.models import Session
from django.contrib import admin


def superviseur(obj):
	return obj.event.supervisor
	
	
def client(obj):
	return obj.customer.username


class SessionAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', client, 'mark', superviseur)
	

admin.site.register(Session, SessionAdmin)
