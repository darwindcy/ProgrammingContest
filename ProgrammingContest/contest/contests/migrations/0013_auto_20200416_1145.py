# Generated by Django 3.0.2 on 2020-04-16 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contests', '0012_contest_stoptime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='contestName',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
