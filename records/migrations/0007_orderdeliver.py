# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-02-11 14:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0006_auto_20170211_2225'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderDeliver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('deliverDate', models.DateField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='records.Order')),
            ],
            options={
                'ordering': ['-created_date'],
            },
        ),
    ]