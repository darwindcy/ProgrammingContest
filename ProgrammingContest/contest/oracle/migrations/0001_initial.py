# Generated by Django 3.0.2 on 2020-02-15 14:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0006_auto_20200215_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='OraclePost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postQuestion', models.TextField(max_length=500)),
                ('postTime', models.DateTimeField(auto_now_add=True)),
                ('postAnswered', models.BooleanField(default=False)),
                ('postUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.User')),
            ],
        ),
    ]
