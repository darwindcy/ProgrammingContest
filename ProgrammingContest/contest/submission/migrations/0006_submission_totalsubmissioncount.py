# Generated by Django 3.0.2 on 2020-03-19 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0005_auto_20200317_1745'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='totalSubmissionCount',
            field=models.IntegerField(default=0),
        ),
    ]
