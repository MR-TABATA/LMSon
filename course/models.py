from django.db import models

class ElmsCourse(models.Model):
  title = models.CharField(verbose_name='タイトル', max_length=200)
  created = models.DateTimeField(verbose_name='生成日', auto_now_add=True)
  modified = models.DateTimeField(verbose_name='更新日', auto_now=True)
  deleted = models.DateTimeField(verbose_name='削除日', blank=True, null=True)
  memo = models.TextField(verbose_name='備考', blank=True, null=True)

  def __str__(self):
    return self.title

  class Meta:
    db_table = 'elms_course'
    verbose_name = 'コース'
    verbose_name_plural = 'コース'