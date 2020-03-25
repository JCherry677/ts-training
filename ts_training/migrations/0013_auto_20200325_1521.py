# Generated by Django 3.0.4 on 2020-03-25 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ts_training', '0012_auto_20200325_1501'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='planned_session',
            name='signup',
        ),
        migrations.AlterField(
            model_name='planned_session',
            name='trainingId',
            field=models.ManyToManyField(to='ts_training.Training_spec'),
        ),
        migrations.AlterField(
            model_name='training_session',
            name='trainingId',
            field=models.ManyToManyField(to='ts_training.Training_spec'),
        ),
    ]
