from django.urls import path
from .views import IndexView, CommitView

app_name = 'query'

urlpatterns = [
  path('', IndexView.as_view(), name='index'),
  path('commit/', CommitView.as_view(), name='commit'),
]