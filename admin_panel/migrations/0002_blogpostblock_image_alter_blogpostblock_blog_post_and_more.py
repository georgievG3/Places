# Generated by Django 5.2.3 on 2025-07-26 08:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpostblock',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='blog_images/'),
        ),
        migrations.AlterField(
            model_name='blogpostblock',
            name='blog_post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocks', to='admin_panel.blogpost'),
        ),
        migrations.DeleteModel(
            name='BlogImages',
        ),
    ]
