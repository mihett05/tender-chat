# Generated by Django 5.0 on 2023-12-10 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0004_contract_solution_diffs'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='contract_type',
            field=models.CharField(choices=[('processed', 'Processed'), ('accepted_customer', 'Accepted Customer'), ('accepted_contractor', 'Accepted Contractor'), ('finished', 'Finished')], default='processed'),
        ),
    ]
