import django
import os
import sys
from django.contrib.auth.hashers import make_password
import random

from faker import Faker
fake = Faker('ja-JP')
Faker.seed(0)

sys.path.append('/path/to/Djangi/project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.develop')

django.setup()
from accounts.models import CustomUser
from chapter.models import ElmsChapterUserShip, ElmsChapter
from lesson.models import ElmsLesson, ElmsLessonUserShip


object_lists = CustomUser.objects.filter(id__gte=38600)
custome_user_chapter_obj = []
for obj in object_lists:
	chapters = ElmsChapter.objects.filter(deleted__isnull=True)
	exam_chapter_obj = []
	for chapter in chapters:
		exam_chapter_obj.append(
			ElmsChapterUserShip(
				custom_user_id=obj.pk,
				chapter_id=chapter.id,
				course_id=chapter.elms_chapter_course_id
			)
		)
	lessons = ElmsLesson.objects.filter(deleted__isnull=True)
	lesson_obj = []
	for lesson in lessons:
		lesson_obj.append(ElmsLessonUserShip(custom_user_id=obj.pk, lesson_id=lesson.id))

	ElmsChapterUserShip.objects.bulk_create(exam_chapter_obj)
	ElmsLessonUserShip.objects.bulk_create(lesson_obj)