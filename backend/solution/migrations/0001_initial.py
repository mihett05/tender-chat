# Generated by Django 5.0 on 2023-12-09 03:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FormPart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.JSONField(default=dict)),
                ('file', models.FileField(upload_to='additional_files/')),
            ],
        ),
        migrations.CreateModel(
            name='Solution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('form_part_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fp1_solution', to='solution.formpart')),
                ('form_part_2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fp2_solution', to='solution.formpart')),
                ('form_part_3', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fp3_solution', to='solution.formpart')),
            ],
        ),
    ]
