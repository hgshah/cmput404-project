# Generated by Django 4.1.2 on 2022-10-29 08:46

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0002_comment_post'),
        ('likes', '0006_alter_inbox_recieved'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='refComment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='comment.comment'),
        ),
        migrations.AlterField(
            model_name='inbox',
            name='recieved',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 29, 8, 46, 11, 328341, tzinfo=datetime.timezone.utc)),
        ),
    ]