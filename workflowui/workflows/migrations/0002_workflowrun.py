# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-21 06:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('workflows', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkflowRun',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('run_id', models.CharField(max_length=50)),
                ('properties', jsonfield.fields.JSONField(default={})),
                ('status', jsonfield.fields.JSONField(blank=True)),
                ('workflow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workflows.Workflow')),
            ],
        ),
    ]
