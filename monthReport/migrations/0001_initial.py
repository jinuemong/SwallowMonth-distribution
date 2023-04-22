# Generated by Django 4.1.6 on 2023-04-12 06:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RecordData',
            fields=[
                ('recordId', models.BigAutoField(help_text='record ID', primary_key=True, serialize=False)),
                ('ranking', models.IntegerField()),
                ('keyDate', models.CharField(max_length=20)),
                ('totalPer', models.IntegerField()),
                ('totalPoint', models.IntegerField()),
                ('activityNum', models.IntegerField()),
                ('clearNum', models.IntegerField()),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recordPost', to=settings.AUTH_USER_MODEL, to_field='userName')),
            ],
        ),
        migrations.CreateModel(
            name='MonthData',
            fields=[
                ('monthId', models.BigAutoField(help_text='month ID', primary_key=True, serialize=False)),
                ('keyDate', models.CharField(max_length=20)),
                ('totalPer', models.IntegerField()),
                ('totalPoint', models.IntegerField()),
                ('doneTask', models.IntegerField()),
                ('clearRoutine', models.IntegerField()),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='monthPost', to=settings.AUTH_USER_MODEL, to_field='userName')),
            ],
        ),
    ]
