# Generated by Django 4.1.2 on 2022-10-29 05:50

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_post_count'),
        ('likes', '0002_inbox_content_inbox_itemtype_inbox_recieved'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='object',
        ),
        migrations.AddField(
            model_name='like',
            name='objectURL',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='post.post'),
        ),
        migrations.AlterField(
            model_name='inbox',
            name='recieved',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 29, 5, 50, 40, 458422, tzinfo=datetime.timezone.utc)),
        ),
    ]
