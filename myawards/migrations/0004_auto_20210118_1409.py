# Generated by Django 3.1.5 on 2021-01-18 12:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myawards', '0003_auto_20210118_1109'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='content',
        ),
        migrations.RemoveField(
            model_name='project',
            name='creativity',
        ),
        migrations.RemoveField(
            model_name='project',
            name='design',
        ),
        migrations.RemoveField(
            model_name='project',
            name='usibalility',
        ),
    ]
