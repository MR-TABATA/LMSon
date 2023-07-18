from django.db import models
from chapter.models import ElmsChapter
from accounts.models import CustomUser
from simple_history.models import HistoricalRecords

def lesson_image_file_path(instance, filename):
  return f'images/lesson/uploads/{filename}'

class ElmsLesson(models.Model):
  title = models.CharField(verbose_name='題目', max_length=200)
  type = models.CharField(verbose_name='種類', max_length=20)
  content = models.TextField(verbose_name='内容', blank=True, null=True)
  timelimit = models.IntegerField(verbose_name='学習時間', blank=True, null=True)
  pass_rate = models.IntegerField(verbose_name='合格点', blank=True, null=True)
  created = models.DateTimeField(verbose_name='生成日時', auto_now_add=True)
  modified = models.DateTimeField(verbose_name='更新日時', auto_now=True)
  deleted = models.DateTimeField(verbose_name='削除日時', blank=True, null=True)
  memo = models.TextField(verbose_name='備考', blank=True, null=True)
  elms_lesson_chapter = models.ForeignKey(ElmsChapter, on_delete=models.CASCADE, related_name='lesson_chapter', verbose_name='単元', )
  elms_lesson_user = models.ManyToManyField(CustomUser, through='ElmsLessonUserShip')
  image = models.ImageField(verbose_name='資料画像', upload_to=lesson_image_file_path, default="images/dummy/dummy_image.jpg")
  history = HistoricalRecords()

  def __str__(self):
    return self.title

  class Meta:
    db_table = 'elms_lesson'
    verbose_name = '講義情報'
    verbose_name_plural = '講義情報'

class ElmsLessonUserShip(models.Model):
  COMPREHENSION_TYPES = (
    ('', '--理解度を選んでください--'),
    (5, 'よく理解できた'),
    (4, 'やや理解できた'),
    (3, 'どちらとも言えない'),
    (2, 'あまり理解できなかった'),
    (1, '全く理解できなかった'),
  )

  lesson = models.ForeignKey(ElmsLesson, on_delete=models.CASCADE)
  custom_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  comprehension = models.IntegerField(verbose_name='理解度', choices=COMPREHENSION_TYPES, blank=True, null=True)
  created = models.DateTimeField(verbose_name='生成日時', auto_now_add=True)
  modified = models.DateTimeField(verbose_name='更新日時', auto_now=True)
  deleted = models.DateTimeField(verbose_name='削除日時', blank=True, null=True)
  history = HistoricalRecords()

  def __str__(self):
    return self.lesson.title

  class Meta:
    db_table = 'elms_lesson_user_ship'
    verbose_name = '講義理解度'
    verbose_name_plural = '講義理解度'

