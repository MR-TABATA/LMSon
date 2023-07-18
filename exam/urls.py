from django.urls import path
from .views import Index, CorrectView

app_name = 'exam'


urlpatterns = [
  path('<int:chapter_id>', Index.as_view(), name='index'),
  path('correct/<int:chapter_id>', CorrectView.as_view(), name='correct'),
]