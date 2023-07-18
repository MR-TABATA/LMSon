from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.forms import TextInput, Textarea
from django.db import models

# Register your models here.
from accounts.models import CustomUser
from chapter.models import ElmsChapter, ElmsChapterUserShip
from lesson.models import ElmsLesson, ElmsLessonUserShip
from exam.models import ElmsExam, ExamUserShip
from notification.models import ElmsNotification
from course.models import ElmsCourse

from import_export.admin import ImportExportModelAdmin
from import_export.admin import ExportMixin
from import_export.formats import base_formats
from dashboard.resource import (
  MyUserResource,
  ElmsCourseResource,
  ElmsChapterResource,
  ElmsExamResource,
  ElmsLessonResource,
  ExamUserShipResource,
  ElmsChapterUserShipResource,
  ElmsLessonUserShipResource,
  ElmsNotificationResource,
)

from django.contrib.auth.hashers import make_password
import re
from django.utils.safestring import mark_safe
from django.utils import timezone


class MyUserChangeForm(UserChangeForm):
  class Meta:
    model = CustomUser
    fields = '__all__'


class MyUserCreationForm(UserCreationForm):
  class Meta:
    model = CustomUser
    fields = ('email','username')


class ExamUserShipInline(admin.TabularInline):
  model = ExamUserShip
  readonly_fields = ['score', 'answer', 'is_right', ]
  exclude = ['exam', 'chapter_id', 'deleted',]
  extra = 0           #　追加行の非表示（未指定の場合、3行表示される）
  max_num=0           #　add another choice（〜の追加）の非表示
  can_delete = False  #　削除チェクボックスの非表示


class ElmsChapterUserShipInline(admin.TabularInline):
  model = ElmsChapterUserShip
  readonly_fields = ['total_score', 'correct_rate', ]
  exclude = ['exam', 'chapter_id', 'deleted', 'course', 'chapter']
  extra = 0           #　追加行の非表示（未指定の場合、3行表示される）
  max_num=0           #　add another choice（〜の追加）の非表示
  can_delete = False  #　削除チェクボックスの非表示


class MyUserAdmin(ImportExportModelAdmin, UserAdmin):
  fieldsets = (
    (_('名前等'), {'fields': ( 'username', 'last_name', 'first_name',)}),
    (_('プロフィール'), {'fields': ('company', 'department', 'position', 'occupation')}),
    (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'password')}),
    (_('生成・更新・削除'), {'fields': ('created', 'modified', 'deleted')}),
  )
  add_fieldsets = (
    (None, {
      'classes': ('wide',),
      'fields': ('email', 'password1', 'password2'),
    }),
  )
  form = MyUserChangeForm
  add_form = MyUserCreationForm
  list_display = ('last_name', 'first_name', 'username', 'email', 'is_staff')
  list_filter = ('is_staff', 'is_superuser', 'is_active')
  search_fields = ('email', 'username')
  readonly_fields = ['created', 'modified', 'deleted']
  ordering = ('id',)
  resource_class = MyUserResource
  inlines = [ ExamUserShipInline, ElmsChapterUserShipInline ]

  def delete(self):
    self.deleted = timezone.now()
    self.save()

  def get_queryset(self, request):
    queryset = super().get_queryset(request)
    return queryset.filter(deleted__isnull=True).all()

  def delete_queryset(self, request, queryset):
    for obj in queryset:
      obj.deleted = timezone.now()
      obj.save()




class ElmsCourseAdmin(ImportExportModelAdmin, admin.ModelAdmin):
  list_display = ('id', 'title', 'created', 'modified')
  list_display_links = ('title',)
  fieldsets = (
    (None, {'fields': ('title', 'memo', 'created', 'modified', 'deleted')}),
  )
  readonly_fields = ['created', 'modified', 'deleted']
  resource_class = ElmsCourseResource
  formats = [base_formats.CSV]
  formfield_overrides = {
    models.CharField: {'widget': TextInput(attrs={'size': '80'})},
    models.TextField: {'widget': Textarea(attrs={'rows': 10, 'cols': 80})},
  }

  def delete(self):
    self.deleted = timezone.now()
    self.save()

  def get_queryset(self, request):
    queryset = super().get_queryset(request)
    return queryset.filter(deleted__isnull=True).all()

  def delete_queryset(self, request, queryset):
    for obj in queryset:
      obj.deleted = timezone.now()
      obj.save()



class ElmsChapterAdmin(ImportExportModelAdmin, admin.ModelAdmin):
  list_display = ('id', 'chapter_title', 'elms_course_title', 'created', 'modified')
  list_display_links = ('chapter_title',)
  fieldsets = (
    (None, {'fields': ('chapter_title', 'elms_course_title', 'memo', 'created', 'modified', 'deleted')}),
  )
  readonly_fields = ['created', 'modified', 'elms_course_title', 'deleted' ]
  resource_class = ElmsChapterResource
  formats = [base_formats.CSV]
  formfield_overrides = {
    models.CharField: {'widget': TextInput(attrs={'size': '80'})},
    models.TextField: {'widget': Textarea(attrs={'rows': 10, 'cols': 80})},
  }
  def elms_course_title(self, obj):
    return obj.elms_chapter_course.title
  elms_course_title.short_description = 'コース名'

  def delete(self):
    self.deleted = timezone.now()
    self.save()

  def get_queryset(self, request):
    queryset = super().get_queryset(request)
    return queryset.filter(deleted__isnull=True).all()

  def delete_queryset(self, request, queryset):
    for obj in queryset:
      obj.deleted = timezone.now()
      obj.save()



class ElmsExamAdmin(ImportExportModelAdmin, admin.ModelAdmin):
  list_display = ('id', 'no_html_exam_body')
  list_display_links = ('no_html_exam_body',)
  def no_html_exam_body(self, obj):
    reg_obj = re.compile(r"<[^>]*?>")
    return reg_obj.sub('', obj.body)
  no_html_exam_body.short_description = '試験内容'
  fieldsets = (
    (None, {'fields': ('body', 'options', 'correct', 'score',  'elms_exam_chapter', 'created', 'modified', 'deleted')}),
  )
  readonly_fields = ['created', 'modified', 'elms_exam_chapter', 'deleted' ]
  resource_class = ElmsExamResource
  formats = [base_formats.CSV]
  formfield_overrides = {
    models.CharField: {'widget': TextInput(attrs={'size': '80'})},
    models.TextField: {'widget': Textarea(attrs={'rows': 10, 'cols': 80})},
  }

  def delete(self):
    self.deleted = timezone.now()
    self.save()

  def get_queryset(self, request):
    queryset = super().get_queryset(request)
    return queryset.filter(deleted__isnull=True).all()

  def delete_queryset(self, request, queryset):
    for obj in queryset:
      obj.deleted = timezone.now()
      obj.save()



class ElmsLessonAdmin(ImportExportModelAdmin, admin.ModelAdmin):
  list_display = ('id', 'title', 'type', 'lesson_image')
  list_display_links = ('title',)
  fieldsets = (
    (None, {'fields': ('title', 'type', 'content', 'timelimit', 'pass_rate', 'memo', 'elms_lesson_chapter', 'image')}),
    (None, {'fields': ('created', 'modified', 'deleted')}),
  )
  def lesson_image(self, obj):
    if obj.image.url :
      return mark_safe('<img src="{}" style="width:100px;height:auto;">'.format(obj.image.url))
  lesson_image.short_description = '資料画像'
  readonly_fields = ['created', 'modified', 'deleted']
  resource_class = ElmsLessonResource
  formats = [base_formats.CSV]
  formfield_overrides = {
    models.CharField: {'widget': TextInput(attrs={'size': '80'})},
    models.TextField: {'widget': Textarea(attrs={'rows': 10, 'cols': 80})},
  }

  def delete(self):
    self.deleted = timezone.now()
    self.save()

  def get_queryset(self, request):
    queryset = super().get_queryset(request)
    return queryset.filter(deleted__isnull=True).all()

  def delete_queryset(self, request, queryset):
    for obj in queryset:
      obj.deleted = timezone.now()
      obj.save()



class ElmsNotificationAdmin(ImportExportModelAdmin, admin.ModelAdmin):
  list_display = ('id', 'target', 'title', )
  list_display_links = ('title',)
  fieldsets = (
    (None, {'fields': ('target', 'title', 'content', 'created', 'modified', 'deleted', )}),
  )
  readonly_fields = ['created', 'modified', 'deleted', ]
  resource_class = ElmsNotificationResource
  formats = [base_formats.CSV]
  formfield_overrides = {
    models.CharField: {'widget': TextInput(attrs={'size': '80'})},
    models.TextField: {'widget': Textarea(attrs={'rows': 50, 'cols': 80})},
  }

  def delete(self):
    self.deleted = timezone.now()
    self.save()

  def get_queryset(self, request):
    queryset = super().get_queryset(request)
    return queryset.filter(deleted__isnull=True).all()

  def delete_queryset(self, request, queryset):
    for obj in queryset:
      obj.deleted = timezone.now()
      obj.save()




class ExamUserShipAdmin(ExportMixin, admin.ModelAdmin):
  list_display = ('elms_exam_chapter_body', 'examination_id', 'examed_name', 'examed_name_id', 'answer', 'score',)
  list_display_links = ('elms_exam_chapter_body', )
  fieldsets = (
    (None, {'fields': ('elms_exam_chapter_body', 'examination_id', 'examed_name', 'examed_name_id', 'answer', 'score',  'created', 'modified', 'deleted',)}),
  )
  readonly_fields = [ 'created', 'modified', 'deleted', ]
  exclude = ['chapter_id', 'deleted', ]
  extra = 0  # 追加行の非表示（未指定の場合、3行表示される）
  max_num = 0  # add another choice（〜の追加）の非表示
  can_delete = False  # 削除チェクボックスの非表示

  formats = [base_formats.CSV]

  def has_add_permission(self, request, obj=None):
    return False
  def has_change_permission(self, request, obj=None):
    return False
  def has_delete_permission(self, request, obj=None):
    return False

  def elms_exam_chapter_body(self, obj):
    return obj.exam.body

  def examination_id(self, obj):
    return obj.exam.pk

  def examed_name(self, obj):
    return obj.custom_user.last_name+' '+obj.custom_user.first_name

  def examed_name_id(self, obj):
    return obj.custom_user.pk

  examination_id.short_description = '試験ID'
  elms_exam_chapter_body.short_description = '試験内容'
  examed_name_id.short_description = '受験者ID'
  examed_name.short_description = '受験者名'
  resource_class = ExamUserShipResource

  def delete(self):
    self.deleted = timezone.now()
    self.save()

  def get_queryset(self, request):
    queryset = super().get_queryset(request)
    return queryset.filter(deleted__isnull=True).all()

  def delete_queryset(self, request, queryset):
    for obj in queryset:
      obj.deleted = timezone.now()
      obj.save()




class ElmsChapterUserShipAdmin(ExportMixin, admin.ModelAdmin):
  list_display = ('elms_chapter_title', 'chapter_id', 'examed_name', 'examed_name_id', 'total_score', 'correct_rate',)
  list_display_links = ('elms_chapter_title',)
  fieldsets = (
    (None, {'fields':('elms_chapter_title', 'chapter_id', 'examed_name', 'examed_name_id', 'total_score', 'correct_rate',)}),
  )
  readonly_fields = ['created', 'modified', 'deleted', ]

  extra = 0  # 追加行の非表示（未指定の場合、3行表示される）
  max_num = 0  # add another choice（〜の追加）の非表示
  can_delete = False  # 削除チェクボックスの非表示

  formats = [base_formats.CSV]

  def has_add_permission(self, request, obj=None):
    return False
  def has_change_permission(self, request, obj=None):
    return False

  def delete(self):
    self.deleted = timezone.now()
    self.save()

  def get_queryset(self, request):
    queryset = super().get_queryset(request)
    return queryset.filter(deleted__isnull=True).all()

  def delete_queryset(self, request, queryset):
    for obj in queryset:
      obj.deleted = timezone.now()
      obj.save()



  def elms_chapter_title(self, obj):
    return obj.chapter.chapter_title

  def chapter_id(self, obj):
    return obj.chapter.pk

  def examed_name(self, obj):
    return obj.custom_user.last_name+' '+obj.custom_user.first_name

  def examed_name_id(self, obj):
    return obj.custom_user.pk

  elms_chapter_title.short_description = '単元タイトル'
  chapter_id.short_description = '単元ID'
  examed_name_id.short_description = '受験者ID'
  examed_name.short_description = '受験者名'
  resource_class = ElmsChapterUserShipResource



class ElmsLessonUserShipAdmin(ExportMixin, admin.ModelAdmin):
  list_display = ('elms_lesson_title', 'lessoned_name', 'comprehension',)
  list_display_links =  ('elms_lesson_title',)
  fieldsets = (
    (None, {'fields': ('elms_lesson_title', 'lessoned_name', 'comprehension','created', 'modified', 'deleted',)}),
  )
  readonly_fields = ['created', 'modified', 'deleted',]

  extra = 0  # 追加行の非表示（未指定の場合、3行表示される）
  max_num = 0  # add another choice（〜の追加）の非表示
  can_delete = False  # 削除チェクボックスの非表示

  formats = [base_formats.CSV]

  def has_add_permission(self, request, obj=None):
    return False
  def has_change_permission(self, request, obj=None):
    return False


  def delete(self):
    self.deleted = timezone.now()
    self.save()

  def get_queryset(self, request):
    queryset = super().get_queryset(request)
    return queryset.filter(deleted__isnull=True).all()

  def delete_queryset(self, request, queryset):
    for obj in queryset:
      obj.deleted = timezone.now()
      obj.save()

  def elms_lesson_title(self, obj):
    return obj.lesson.title

  def lessoned_name(self, obj):
    return obj.custom_user.last_name + ' ' + obj.custom_user.first_name

  elms_lesson_title.short_description = '講義名'
  lessoned_name.short_description = '受講者'

  resource_class = ElmsLessonUserShipResource



admin.site.register(CustomUser, MyUserAdmin)
admin.site.register(ElmsChapter, ElmsChapterAdmin)
admin.site.register(ElmsCourse, ElmsCourseAdmin)
admin.site.register(ElmsLesson, ElmsLessonAdmin)
admin.site.register(ElmsExam, ElmsExamAdmin)
admin.site.register(ElmsNotification, ElmsNotificationAdmin)
admin.site.register(ExamUserShip, ExamUserShipAdmin)
admin.site.register(ElmsChapterUserShip, ElmsChapterUserShipAdmin)
admin.site.register(ElmsLessonUserShip, ElmsLessonUserShipAdmin)

