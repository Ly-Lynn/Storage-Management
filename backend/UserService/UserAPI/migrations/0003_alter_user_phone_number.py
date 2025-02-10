# Generated by Django 5.1.4 on 2025-02-06 10:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserAPI', '0002_alter_user_managers_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=10, unique=True, validators=[django.core.validators.RegexValidator(message='Phone number must be 10 digits only.', regex='^\\d{10}$')]),
        ),
    ]
