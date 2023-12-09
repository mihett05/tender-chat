from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class FormPart(models.Model):
    data = models.JSONField(default=dict)
    file = models.FileField(upload_to='additional_files/')


class Solution(models.Model):
    form_part_1 = models.ForeignKey(FormPart, on_delete=models.CASCADE, related_name='fp1_solution')
    form_part_2 = models.ForeignKey(FormPart, on_delete=models.CASCADE, related_name='fp2_solution')
    form_part_3 = models.ForeignKey(FormPart, on_delete=models.CASCADE, related_name='fp3_solution')
