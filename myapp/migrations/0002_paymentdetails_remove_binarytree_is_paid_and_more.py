# Generated by Django 4.0.4 on 2022-06-10 11:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_paid', models.BooleanField(default=False)),
                ('amount', models.IntegerField(default=0)),
                ('payment_done_requested', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='binarytree',
            name='is_paid',
        ),
        migrations.AddField(
            model_name='binarytree',
            name='payment',
            field=models.ManyToManyField(related_name='+', through='myapp.PaymentDetails', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='paymentdetails',
            name='binarytree',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.binarytree'),
        ),
        migrations.AddField(
            model_name='paymentdetails',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]