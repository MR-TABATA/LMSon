from django.views import generic
from notification.models import ElmsNotification
from django.views.generic import ListView, DetailView, View

class HomeIndexView(ListView):
  model = ElmsNotification
  queryset = ElmsNotification.objects.filter(deleted__isnull=True, target=1).order_by('-id').all()
  template_name = 'home/index.html'

class OverviewView(generic.TemplateView):
  template_name = 'home/overview.html'