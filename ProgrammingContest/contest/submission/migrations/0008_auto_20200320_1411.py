# Generated by Django 3.0.2 on 2020-03-20 19:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('submission', '0007_auto_20200319_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='submissionTeam',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='submittedBy', to=settings.AUTH_USER_MODEL),
        ),
    ]
