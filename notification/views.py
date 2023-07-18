from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ElmsNotification
from core.utilities import getNotifications


class Index(LoginRequiredMixin, ListView):
  model = ElmsNotification
  queryset = ElmsNotification.objects.filter(deleted__isnull=True, target=0).order_by('-id').all()
  template_name = 'notification/index.html'


class Detail(LoginRequiredMixin, DetailView):
  def get(self, request, *args, **kwargs):
    context = {}
    context['detail']         = ElmsNotification.objects.filter(deleted__isnull=True, id=self.kwargs['pk']).first()
    context['notifications'] = getNotifications()
    return render(request, 'notification/detail.html', context)

