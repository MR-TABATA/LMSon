from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, get_user_model
from django.utils.text import capfirst
from django.utils.translation import gettext_lazy as _

UserModel = get_user_model()

class EmailAuthenticationForm(forms.Form):
  email = forms.EmailField(label=_("Email"), max_length=254, widget=forms.TextInput(attrs={'autofocus': True}))
  password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput)
  error_messages = {
      'invalid_login': "メールアドレスまたはパスワードに誤りがあります",
      'inactive': _("This account is inactive"),
  }

  def __init__(self, request=None, *args, **kwargs):
    self.request = request
    self.user_cache = None
    super().__init__(*args, **kwargs)
    self.email_field = UserModel._meta.get_field("email")
    if self.fields["email"].label is None:
      self.fields["email"].label = capfirst(self.email_field.verbose_name)

  def clean(self):
    email = self.cleaned_data.get("email")
    password = self.cleaned_data.get("password")
    if email is not None and password:
      self.user_cache = authenticate(self.request, email=email, password=password)
      if self.user_cache is None:
        raise forms.ValidationError(
          self.error_messages['invalid_login'],
          code='invalid_login',
          params={"email": self.email_field.verbose_name}
        )
      else:
        self.confirm_login_allowed(self.user_cache)
      return self.cleaned_data

  def confirm_login_allowed(self, user):
      if not user.is_active:
        raise forms.ValidationError(self.error_messages["inactive"], code='inactive')

  def get_user_id(self):
      if self.user_cache:
        return self.user_cache.id
      return None

  def get_user(self):
      return self.user_cache

class PasswordModifyForm(PasswordChangeForm):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for field in self.fields.values():
      field.widget.attrs['class'] = 'form-control'

class ProfileUpdateForm(forms.ModelForm):
  """ユーザー情報更新フォーム"""

  class Meta:
    model = UserModel
    fields = ('last_name', 'first_name', 'username', 'mobile', 'email', 'company', 'department', 'position', 'occupation', 'avater')
    labels = {
      'first_name' : '名前',
      'last_name'  : '苗字',
      'username'   : 'ユーザー名',
      'mobile'     : '携帯電話',
      'email'      : 'メールアドレス',
      'company'    : '会社',
      'department' : '所属',
      'position'   : '役職',
      'occupation' : '職種',
      'avater'     : 'プロフィール画像',
    }

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for field in self.fields.values():
      field.widget.attrs['class'] = 'form-control'