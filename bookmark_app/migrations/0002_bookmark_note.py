# Generated by Django 3.2.18 on 2023-04-09 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookmark_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookmark',
            name='note',
            field=models.TextField(blank=True),
        ),
    ]