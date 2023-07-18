from django.shortcuts import render
from django.views.generic import DetailView, CreateView, View
from .models import ElmsLesson, ElmsLessonUserShip
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from .forms import ComprehensionChoiceForm
from django.views.generic.edit import FormView
from core.utilities import getNotifications
from django.utils import timezone


class Index(LoginRequiredMixin, FormView):
	model = ElmsLesson
	form_class = ComprehensionChoiceForm
	template_name = 'lesson/index.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["lesson"] = ElmsLesson.objects.filter(deleted__isnull=True, id=self.kwargs['pk']).first()
		context['lesson_user'] = ElmsLessonUserShip.objects.filter(deleted__isnull=True, lesson_id=self.kwargs['pk'],
																															 custom_user_id=self.request.user.pk).first()
		context['notifications'] = getNotifications()
		return context


class HistoryView(LoginRequiredMixin, CreateView):
	def get(self, request, *args, **kwargs):
		elms_lesson_user = ElmsLessonUserShip.objects.filter(deleted__isnull=True, lesson_id=self.kwargs['pk'], custom_user=self.request.user.pk).first()
		elms_lesson_user = ElmsLessonUserShip.objects.get(pk=elms_lesson_user.id)
		elms_lesson_user.comprehension = request.GET.get("comprehension")
		elms_lesson_user.modified = timezone.now()
		elms_lesson_user.save()

		return redirect('lesson:index', pk=self.kwargs['pk'])

