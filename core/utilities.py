from django.db import connection
from notification.models import ElmsNotification

def getNotifications():
	model = ElmsNotification
	return ElmsNotification.objects.filter(deleted__isnull=True, target=0).order_by('-id').all()[:5]
