# Generated by Django 3.0.2 on 2020-04-24 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0014_auto_20200424_0914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='submissionTime',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
