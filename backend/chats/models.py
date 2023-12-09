from django.contrib.auth import get_user_model
from django.db import models

from solution.models import Solution, FormPart

User = get_user_model()


class CommitTypes(models.TextChoices):
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    PROCESSED = 'processed'


class Contract(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_chats')
    contractor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contractor_chats')
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE, related_name='contract')


class Commit(models.Model):
    form_part_data = models.ForeignKey(FormPart, on_delete=models.CASCADE, related_name='commit')
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='commits')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_commits')
    parent = models.ForeignKey(
        'Commit', on_delete=models.DO_NOTHING,
        default=None, null=True, blank=True,
        related_name='previous_commit'
    )
    status = models.CharField(choices=CommitTypes.choices, default=CommitTypes.PROCESSED)
    comment = models.CharField()


class Message(models.Model):
    text = models.CharField()
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_messages')
