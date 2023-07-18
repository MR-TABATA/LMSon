from django.db import models
from course.models import ElmsCourse
from accounts.models import CustomUser
from simple_history.models import HistoricalRecords

class ElmsChapter(models.Model):
  chapter_title = models.CharField(verbose_name='単元タイトル', max_length=200)
  created = models.DateTimeField(verbose_name='生成日時', auto_now_add=True)
  modified = models.DateTimeField(verbose_name='更新日時', auto_now=True)
  deleted = models.DateTimeField(verbose_name='削除日時', blank=True, null=True)
  memo = models.TextField(verbose_name='備考', blank=True, null=True)
  elms_chapter_course = models.ForeignKey(ElmsCourse, on_delete=models.CASCADE, related_name='chapter_course')
  history = HistoricalRecords()

  def __str__(self):
    return self.chapter_title

  class Meta:
    db_table = 'elms_chapter'
    verbose_name = '単元情報'
    verbose_name_plural = '単元情報'

class ElmsChapterUserShip(models.Model):
  chapter = models.ForeignKey(ElmsChapter, on_delete=models.CASCADE)
  custom_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  course = models.ForeignKey(ElmsCourse, on_delete=models.CASCADE)
  total_score = models.IntegerField(verbose_name='総得点', blank=True, null=True)
  correct_rate = models.CharField(verbose_name='正答率', max_length=20)
  created = models.DateTimeField(verbose_name='生成日時', auto_now_add=True)
  modified = models.DateTimeField(verbose_name='更新日時', auto_now=True)
  deleted = models.DateTimeField(verbose_name='削除日時', blank=True, null=True)
  history = HistoricalRecords()

  def __str__(self):
    return self.chapter.chapter_title

  class Meta:
    db_table = 'elms_chapter_user'
    verbose_name = '試験サマリ'
    verbose_name_plural = '試験サマリ'

