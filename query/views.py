from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView
from .forms import ElmsQueryForms
from .models import ElmsQuery


# Create your views here.
class IndexView(CreateView):
  template_name = "query/index.html"
  form_class = ElmsQueryForms
  success_url = reverse_lazy("query:commit")

class CommitView(TemplateView):
  template_name = "query/commit.html"