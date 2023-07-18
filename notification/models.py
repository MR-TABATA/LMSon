from django.db import models
from accounts.models import CustomUser
from simple_history.models import HistoricalRecords
from django.utils import timezone

# Create your models here.


class ElmsNotification(models.Model):
  TARGET_CHOICE = (
    (1, 'ログイン前のトップに公開'),
    (0, 'ログイン後表示'),
  )
  target = models.IntegerField(verbose_name='お知らせ掲載場所', choices=TARGET_CHOICE, blank=True, null=True)
  title = models.CharField(verbose_name='お知らせ題', max_length=200)
  content = models.TextField(verbose_name='お知らせ内容', )
  created = models.DateTimeField(verbose_name='生成日時', auto_now_add=True)
  modified = models.DateTimeField(verbose_name='更新日時', auto_now=True)
  deleted = models.DateTimeField(verbose_name='削除日時', blank=True, null=True)
  elms_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notificated_user')
  history = HistoricalRecords()

  def __str__(self):
    return self.title

  class Meta:
    db_table = 'elms_notification'
    verbose_name = 'お知らせ情報'
    verbose_name_plural = 'お知らせ情報'




