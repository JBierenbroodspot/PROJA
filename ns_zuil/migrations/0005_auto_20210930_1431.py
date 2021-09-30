# Generated by Django 3.2.7 on 2021-09-30 12:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ns_zuil', '0004_auto_20210929_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='moderated_by_fk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Moderated by'),
        ),
        migrations.AlterField(
            model_name='message',
            name='moderation_datetime',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Moderated on'),
        ),
        migrations.AlterField(
            model_name='message',
            name='post_datetime',
            field=models.DateTimeField(auto_now=True, verbose_name='Posted on'),
        ),
        migrations.AlterField(
            model_name='message',
            name='station_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ns_zuil.station', verbose_name='Station'),
        ),
        migrations.AlterField(
            model_name='message',
            name='status',
            field=models.CharField(default='PENDING', max_length=20),
        ),
    ]
