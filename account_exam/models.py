from django.db import models


class AccountExam(models.Model):
    account_id = models.IntegerField(blank=True, null=True)
    exam_id = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField()
    modified = models.DateTimeField(blank=True, null=True)
    deleted = models.DateTimeField(blank=True, null=True)
    memo = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'account_exam'