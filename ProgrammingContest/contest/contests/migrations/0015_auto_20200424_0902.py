# Generated by Django 3.0.2 on 2020-04-24 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contests', '0014_auto_20200416_1216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='pauseTime',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='contest',
            name='startTime',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='contest',
            name='stopTime',
            field=models.DateTimeField(null=True),
        ),
    ]
