# Generated by Django 4.1.2 on 2022-11-04 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inbox', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InboxPOSTObject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_type', models.CharField(default='undef', max_length=400)),
            ],
        ),
    ]
