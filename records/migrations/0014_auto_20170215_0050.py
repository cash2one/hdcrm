# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-02-14 16:50
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('records', '0013_client_ranking'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('note', models.TextField()),
                ('nextDate', models.DateField()),
            ],
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-created_date']},
        ),
        migrations.AlterField(
            model_name='client',
            name='ranking',
            field=models.CharField(choices=[(b'A', '\u5f00\u53d1\u9636\u6bb5'), (b'B', '\u6b63\u5e38\u64cd\u4f5c\u9636\u6bb5'), (b'C', '\u91cd\u70b9\u5ba2\u6237')], default=b'A', max_length=10),
        ),
        migrations.AddField(
            model_name='clientlog',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='records.Client'),
        ),
        migrations.AddField(
            model_name='clientlog',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
