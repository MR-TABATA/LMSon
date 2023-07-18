from django import forms
from .models import ElmsLessonUserShip

class ComprehensionChoiceForm(forms.ModelForm):
  class Meta:
    model = ElmsLessonUserShip
    fields = ("comprehension", )
    labels = {"comprehension": "",}
    initial = {"comprehension": "",}

