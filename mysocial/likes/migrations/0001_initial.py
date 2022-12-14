# Generated by Django 4.1.2 on 2022-11-23 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.JSONField()),
                ('author_id', models.TextField()),
                ('object', models.TextField()),
                ('object_type', models.CharField(choices=[('post', 'Post'), ('comment', 'Comment')], max_length=20)),
            ],
            options={
                'unique_together': {('author_id', 'object')},
            },
        ),
    ]
