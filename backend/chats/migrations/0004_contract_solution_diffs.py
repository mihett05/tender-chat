# Generated by Django 5.0 on 2023-12-10 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0003_remove_message_contract_message_commit'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='solution_diffs',
            field=models.JSONField(default=dict),
        ),
    ]
