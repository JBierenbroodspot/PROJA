# Generated by Django 3.2.7 on 2021-09-29 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ns_zuil', '0002_auto_20210928_1628'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='message',
            field=models.CharField(default='', max_length=140),
            preserve_default=False,
        ),
    ]
