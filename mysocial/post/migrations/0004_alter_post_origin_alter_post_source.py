# Generated by Django 4.1.2 on 2022-11-20 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_post_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='origin',
            field=models.CharField(default='www.default.com', max_length=500),
        ),
        migrations.AlterField(
            model_name='post',
            name='source',
            field=models.CharField(default='www.default.com', max_length=500),
        ),
    ]