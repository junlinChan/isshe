# Generated by Django 3.0.3 on 2020-03-03 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servers', '0007_auto_20200303_1051'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='hostname',
            field=models.CharField(blank=True, db_index=True, default=None, help_text='主机名', max_length=50, verbose_name='主机名'),
        ),
    ]
