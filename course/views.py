from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from .models import ElmsCourse
from django.contrib.auth.mixins import LoginRequiredMixin


class Index(LoginRequiredMixin, ListView):
  model = ElmsCourse
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    return context
  queryset = ElmsCourse.objects.filter(deleted__isnull=True)
  template_name = 'course/index.html'