# Generated by Django 3.0.2 on 2020-03-22 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contests', '0010_auto_20200302_1225'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='startTime',
            field=models.TimeField(null=True),
        ),
    ]
