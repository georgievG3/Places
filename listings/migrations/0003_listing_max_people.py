# Generated by Django 5.2.3 on 2025-07-12 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0002_remove_location_name_listing_mini_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='max_people',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
