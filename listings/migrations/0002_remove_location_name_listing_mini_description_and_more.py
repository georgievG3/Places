# Generated by Django 5.2.3 on 2025-07-09 19:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='name',
        ),
        migrations.AddField(
            model_name='listing',
            name='mini_description',
            field=models.CharField(default='wow', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='listing',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='listings.location'),
        ),
    ]
