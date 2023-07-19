from django import forms
from .models import ElmsQuery

class ElmsQueryForms(forms.ModelForm):
  class Meta:
    model = ElmsQuery
    fields = ['mail', 'content',]

  def __init__(self, *args, **kwargs):
    for field in self.base_fields.values():
      field.widget.attrs["class"] = "form-control"
    super().__init__(*args, **kwargs)