# Generated by Django 5.0 on 2023-12-09 08:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='commit',
        ),
    ]