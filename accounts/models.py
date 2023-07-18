from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
import hashlib
from simple_history.models import HistoricalRecords


class UserManager(BaseUserManager):
	use_in_migrations = True

	def _create_user(self, username, email, password, **extra_fields):
		if not email:
			raise ValueError('Emailを入力して下さい')
		email = self.normalize_email(email)
		username = self.model.normalize_username(username)
		user = self.model(username=username, email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self.db)
		return user

	def create_user(self, username, email, password=None, **extra_fields):
		extra_fields.setdefault('is_staff', False)
		extra_fields.setdefault('is_superuser', False)
		return self._create_user(email, password, **extra_fields)

	def create_superuser(self, username, email, password, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)
		if extra_fields.get('is_staff') is not True:
			raise ValueError('is_staff=Trueである必要があります。')
		if extra_fields.get('is_superuser') is not True:
			raise ValueError('is_superuser=Trueである必要があります。')
		return self._create_user(username, email, password, **extra_fields)


def avater_file_path(instance, filename):
  hash = hashlib.sha256(str(instance.id).encode()).hexdigest()
  return f'images/icons/{hash}/{filename}'

class CustomUser(AbstractBaseUser, PermissionsMixin):
	username_validator = UnicodeUsernameValidator()

	username = models.CharField(_("username"), max_length=50, validators=[username_validator], blank=True)
	mobile = models.CharField(_("携帯"), max_length=20, blank=True)
	first_name = models.CharField(_("名"), max_length=50, blank=True)
	last_name = models.CharField(_("姓"), max_length=50, blank=True)
	email = models.EmailField(_("メール"), unique=True)
	company = models.CharField(_("会社名"), max_length=100, blank=True)
	department = models.CharField(_("所属"), max_length=100, blank=True)
	position = models.CharField(_("役職"), max_length=100, blank=True)
	occupation = models.CharField(_("職種"), max_length=100, blank=True)
	avater = models.ImageField(upload_to=avater_file_path)


	#prefecture = models.CharField(_("住所（都道府県）"), max_length=50, blank=True)
	#postcode = models.CharField(_("郵便番号"), max_length=10, blank=True)
	#city = models.CharField(_("住所（市区）"), max_length=50, blank=True)
	#locality = models.CharField(_("住所（町村）"), max_length=50, blank=True)
	#block = models.CharField(_("住所（番地）"), max_length=50, blank=True)
	#building = models.CharField(_("住所（建物名・部屋番号）"), max_length=100, blank=True)

	is_staff = models.BooleanField(_("staff status"), default=False)
	is_active = models.BooleanField(_("active"), default=True)
	date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
	created = models.DateTimeField(verbose_name='生成日時', auto_now_add=True)
	modified = models.DateTimeField(verbose_name='更新日時', auto_now=True)
	deleted = models.DateTimeField(verbose_name='削除日時', blank=True, null=True)
	delete_memo = models.TextField(verbose_name='削除理由', blank=True, null=True)
	history = HistoricalRecords()

	objects = UserManager()
	USERNAME_FIELD = "email"
	EMAIL_FIELD = "email"
	REQUIRED_FIELDS = ['username']

	class Meta:
		verbose_name = _("user")
		verbose_name_plural = _("users")

	def clean(self):
		super().clean()
		self.email = self.__class__.objects.normalize_email(self.email)

	def email_user(self, subject, message, from_email=None, **kwargs):
		send_mail(subject, message, from_email, [self.email], **kwargs)
