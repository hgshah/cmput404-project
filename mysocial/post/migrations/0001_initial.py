# Generated by Django 4.1.2 on 2022-10-20 20:44

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('official_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=500)),
                ('source', models.CharField(blank=True, max_length=500)),
                ('origin', models.CharField(blank=True, max_length=500)),
                ('published', models.DateTimeField(default=datetime.datetime.now)),
                ('description', models.CharField(blank=True, max_length=500)),
                ('unlisted', models.BooleanField(default=False)),
                ('visibility', models.CharField(choices=[('friends', 'Friends'), ('public', 'Public')], default='public', max_length=20)),
                ('contentType', models.CharField(choices=[('text/markdown', 'Common Mark'), ('text/plain', 'Plain'), ('application/base64', 'Application'), ('image/png;base64', 'Embedded Png'), ('image/jpeg;base64', 'Embedded Jpeg')], default='text/plain', max_length=20)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
