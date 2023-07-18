from django.urls import path
from .views import Index, HistoryView

app_name = 'lesson'


urlpatterns = [
  path('<int:pk>', Index.as_view(), name='index'),
  path('history/<int:pk>', HistoryView.as_view(), name='history'),
]