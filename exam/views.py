from django.shortcuts import render
from django.views.generic import CreateView, ListView
from .models import ElmsExam, ExamUserShip
from chapter.models import ElmsChapter, ElmsChapterUserShip
from django.contrib.auth.mixins import LoginRequiredMixin

from django.utils import timezone
from core.utilities import getNotifications

# Create your views here.
class Index(LoginRequiredMixin, ListView):
  template_name = 'exam/index.html'
  model = ElmsExam

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['examinations'] = ElmsExam.objects.filter(deleted__isnull=True, elms_exam_chapter=self.kwargs['chapter_id'])
    context['exam_first'] = ElmsExam.objects.filter(deleted__isnull=True, elms_exam_chapter=self.kwargs['chapter_id']).first()
    context['exam_last'] = ElmsExam.objects.filter(deleted__isnull=True, elms_exam_chapter=self.kwargs['chapter_id']).last()
    context['chapter'] = ElmsChapter.objects.filter(deleted__isnull=True, id=self.kwargs['chapter_id']).first()
    context['notifications'] = getNotifications()

    return context


class CorrectView(LoginRequiredMixin, CreateView):
  template_name = 'exam/result.html'
  model = ExamUserShip
  fields = ("exam", "custom_user", "answer", "is_right", "chapter_id", "score")

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    if not ExamUserShip.objects.filter(deleted__isnull=True, custom_user=self.request.user.pk, chapter_id=self.kwargs['chapter_id']).exists():
      total_score=total_correct=cnt=0
      correct_rate=''
      for i in range(int(self.request.POST.get("first")), int(self.request.POST.get("last"))+1):
        post_exam = "exam" + str(i)
        #解答と正解が一致した場合、is_rightをtrueにし、scoreをexam.scoreで上書き
        exam_rs_right = False
        exam_rs_score = 0
        exam_rs = ElmsExam.objects.filter(deleted__isnull=True, pk=i, correct=self.request.POST.get(post_exam)).first()
        if exam_rs:
          exam_rs_right=True
          exam_rs_score=exam_rs.score
          total_correct+=1
        ExamUserShip.objects.create(
          exam_id=i,
          custom_user_id=self.request.user.pk,
          answer=self.request.POST.get(post_exam),
          is_right=exam_rs_right,
          score=exam_rs_score,
          chapter_id=self.kwargs['chapter_id'],
        )
        total_score+=exam_rs_score
        cnt+=1
        correct_rate=str(total_correct)+"/"+str(cnt)
      chapter = ElmsChapter.objects.filter(deleted__isnull=True, id=self.kwargs['chapter_id']).first()
      elms_chapter_user = ElmsChapterUserShip.objects.filter(deleted__isnull=True, chapter_id=self.kwargs['chapter_id'], custom_user=self.request.user.pk).first()
      chapter_user_ship = ElmsChapterUserShip.objects.get(pk=elms_chapter_user.id)
      chapter_user_ship.total_score = total_score
      chapter_user_ship.correct_rate = correct_rate
      chapter_user_ship.modified = timezone.now()
      chapter_user_ship.save()

    context['chapter'] = ElmsChapter.objects.filter(deleted__isnull=True, id=self.kwargs['chapter_id']).first()
    context['results'] = ExamUserShip.objects.filter(deleted__isnull=True, custom_user=self.request.user.pk, chapter_id=self.kwargs['chapter_id']).select_related()
    context['notifications'] = getNotifications()
    return context


