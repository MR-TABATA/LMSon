from django.urls import path
from .views import Index, Detail

app_name = 'notification'

urlpatterns = [
  path('', Index.as_view(), name='index'),
  path('detail/<int:pk>', Detail.as_view(), name='detail'),

]