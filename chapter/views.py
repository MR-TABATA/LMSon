from django.shortcuts import render
from django.views.generic import ListView
from course.models import ElmsCourse
from .models import ElmsChapter, ElmsChapterUserShip
from lesson.models import ElmsLesson, ElmsLessonUserShip
from exam.models import ElmsExam, ExamUserShip
from django.contrib.auth.mixins import LoginRequiredMixin
from core.utilities import getNotifications

class Index(LoginRequiredMixin, ListView):
  def get(self, request, *args, **kwargs):
    context = {}
    context['chapters'] = ElmsChapter.objects.filter(deleted__isnull=True)
    """
    elms_lesson_user_shipにログイン者のデータがなかったら
    lessonを、elms_lesson_user_shipに
    examを、elms_exam_user_shipにインポート
    """
    is_chapter_exam = ElmsChapterUserShip.objects.filter(deleted__isnull=True, custom_user=self.request.user.pk).first()
    if not is_chapter_exam:
      lessons = ElmsLesson.objects.filter(deleted__isnull=True)
      lesson_obj = []
      for lesson in lessons:
        lesson_obj.append(ElmsLessonUserShip(custom_user_id=self.request.user.pk, lesson_id=lesson.id))
      ElmsLessonUserShip.objects.bulk_create(lesson_obj)

      exam_chapter_obj = []
      for chapter in context['chapters']:
        exam_chapter_obj.append(ElmsChapterUserShip(custom_user_id=self.request.user.pk, chapter_id=chapter.id, course_id=chapter.elms_chapter_course_id))
      ElmsChapterUserShip.objects.bulk_create(exam_chapter_obj)

    context['courses'] = ElmsCourse.objects.filter(deleted__isnull=True)
    context['chapters'] = ElmsChapter.objects.filter(deleted__isnull=True)
    context['lessons'] = ElmsLesson.objects.filter(deleted__isnull=True)
    context['notifications'] = getNotifications()
    return render(request, 'chapter/index.html', context)



