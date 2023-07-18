from django.db import models
from chapter.models import ElmsChapter
from accounts.models import CustomUser
import re
from simple_history.models import HistoricalRecords

# Create your models here.
class ElmsExam(models.Model):
  question_type = models.CharField(verbose_name='種類', max_length=20)
  title = models.CharField(verbose_name='タイトル', max_length=200)
  body = models.CharField(verbose_name='試験内容', max_length=200)
  options = models.TextField(verbose_name='回答', blank=True, null=True)
  correct = models.IntegerField(verbose_name='正解', )
  score = models.IntegerField(verbose_name='点数', )
  explain = models.TextField(verbose_name='説明', blank=True, null=True)
  comment = models.TextField(verbose_name='備考', blank=True, null=True)
  created = models.DateTimeField(verbose_name='生成日時', auto_now_add=True)
  modified = models.DateTimeField(verbose_name='更新日時', auto_now=True)
  deleted = models.DateTimeField(verbose_name='削除日時', blank=True, null=True)
  elms_exam_chapter = models.ForeignKey(ElmsChapter, on_delete=models.CASCADE, related_name='exam_chapter', verbose_name='章・単元', )
  elms_exam_user = models.ManyToManyField(CustomUser, through='ExamUserShip')
  history = HistoricalRecords()

  def __str__(self):
    return self.title

  class Meta:
    db_table = 'elms_exam'
    verbose_name = '試験情報'
    verbose_name_plural = '試験情報'


class ExamUserShip(models.Model):
  exam = models.ForeignKey(ElmsExam, on_delete=models.CASCADE, verbose_name='試験',)
  custom_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='受験者', )
  answer = models.IntegerField(blank=True, null=True, verbose_name='回答',)
  chapter_id = models.IntegerField(blank=True, null=True)
  is_right = models.BooleanField(default=False, verbose_name='判定',)
  score = models.IntegerField(default=0, verbose_name='点数',)
  created = models.DateTimeField(verbose_name='生成日時', auto_now_add=True)
  modified = models.DateTimeField(verbose_name='更新日時', auto_now=True)
  deleted = models.DateTimeField(verbose_name='削除日時', blank=True, null=True)
  history = HistoricalRecords()

  def __str__(self):
    reg_obj = re.compile(r"<[^>]*?>")
    return reg_obj.sub('', self.exam.body)

  class Meta:
    db_table = 'elms_exam_user_ship'
    verbose_name = '受験者と成績'
    verbose_name_plural = '受験者と成績'



