# Generated by Django 3.0.2 on 2020-02-15 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contests', '0002_auto_20200214_2256'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='participatingIn',
            field=models.ManyToManyField(blank=True, to='contests.Contest'),
        ),
        migrations.CreateModel(
            name='customUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userName', models.CharField(max_length=30, unique=True)),
                ('userType', models.CharField(choices=[('administrator', 'ADMINISTRATOR'), ('participant', 'PARTICIPANT'), ('grader', 'GRADER')], default='participant', max_length=20)),
                ('password', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('date_joined', models.DateTimeField()),
                ('last_login', models.DateTimeField()),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('participatingIn', models.ManyToManyField(blank=True, to='contests.Contest')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
