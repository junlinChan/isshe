# Generated by Django 3.0.3 on 2020-03-02 14:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('servers', '0004_auto_20200302_2242'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='server',
            name='password',
        ),
        migrations.RemoveField(
            model_name='server',
            name='username',
        ),
    ]
