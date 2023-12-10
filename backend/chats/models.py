from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.db import models

User = get_user_model()


class CommitTypes(models.TextChoices):
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    PROCESSED = 'processed'
    FINISHED = 'finished'


class Contract(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_chats')
    contractor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contractor_chats')
    solution = models.JSONField(default=dict)
    solution_diffs = models.JSONField(default=dict)


class Attachments(models.Model):
    file = models.FileField(upload_to='attachments/')
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='attachments')


class Commit(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_commits')
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='commits')
    current_solution = models.JSONField(default=dict)
    parent = models.ForeignKey(
        'Commit', on_delete=models.DO_NOTHING,
        default=None, null=True, blank=True,
        related_name='previous_commit'
    )
    status = models.CharField(choices=CommitTypes.choices, default=CommitTypes.PROCESSED)
    attachments = ArrayField(models.IntegerField(), default=list)


class Message(models.Model):
    text = models.CharField()
    # contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_messages')
    commit = models.ForeignKey(Commit, on_delete=models.CASCADE, default=None, related_name='messages')
