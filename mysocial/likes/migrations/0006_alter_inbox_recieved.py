# Generated by Django 4.1.2 on 2022-10-29 08:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('likes', '0005_alter_inbox_recieved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inbox',
            name='recieved',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 29, 8, 10, 3, 578657, tzinfo=datetime.timezone.utc)),
        ),
    ]