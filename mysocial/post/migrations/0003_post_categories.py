# Generated by Django 4.1.2 on 2022-11-12 04:40

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_post_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='categories',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=30), default=list, size=None),
        ),
    ]
