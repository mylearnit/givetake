# Generated by Django 4.0.4 on 2022-06-07 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='total_give_help',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='total_pmf',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='total_received_help',
            field=models.FloatField(default=0),
        ),
    ]
