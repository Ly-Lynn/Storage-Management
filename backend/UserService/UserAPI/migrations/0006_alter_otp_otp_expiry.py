# Generated by Django 5.1.4 on 2025-02-06 10:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserAPI', '0005_alter_otp_otp_expiry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='otp_expiry',
            field=models.DateTimeField(default=datetime.datetime(2025, 2, 6, 11, 4, 42, 7438, tzinfo=datetime.timezone.utc)),
        ),
    ]
