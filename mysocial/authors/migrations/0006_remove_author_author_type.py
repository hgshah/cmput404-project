# Generated by Django 4.1.2 on 2022-11-17 06:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0005_rename_password_remotenode_remote_password_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='author_type',
        ),
    ]