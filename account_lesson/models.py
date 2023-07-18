from django.db import models


class AccountLesson(models.Model):
    account_id = models.IntegerField(blank=True, null=True)
    lesson_id = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField()
    modified = models.DateTimeField(blank=True, null=True)
    deleted = models.DateTimeField(blank=True, null=True)
    memo = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'account_lesson'