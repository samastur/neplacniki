# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-09-25 14:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shirkers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.TextField(db_index=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='vat_id',
            field=models.CharField(db_index=True, max_length=8),
        ),
    ]
