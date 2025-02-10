# Generated by Django 5.1.4 on 2025-02-06 10:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserAPI', '0003_alter_user_phone_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='otp',
            name='user',
        ),
        migrations.AddField(
            model_name='otp',
            name='email',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='otp',
            name='otp_expiry',
            field=models.DateTimeField(default=datetime.datetime(2025, 2, 6, 11, 0, 17, 482323, tzinfo=datetime.timezone.utc)),
        ),
    ]
