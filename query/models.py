from django.db import models
from simple_history.models import HistoricalRecords

# Create your models here.

class ElmsQuery(models.Model):
	mail = models.CharField(verbose_name='メールアドレス', max_length=200)
	content = models.TextField(verbose_name='問い合わせ内容', blank=True, null=True)
	created = models.DateTimeField(verbose_name='生成日時', auto_now_add=True)
	modified = models.DateTimeField(verbose_name='更新日時', auto_now=True)
	deleted = models.DateTimeField(verbose_name='削除日時', blank=True, null=True)

	def __str__(self):
		return self.content

	class Meta:
		db_table = 'elms_query'
		verbose_name = '問い合わせ情報'
		verbose_name_plural = '問い合わせ情報'