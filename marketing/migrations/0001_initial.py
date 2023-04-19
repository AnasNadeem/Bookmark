# Generated by Django 3.2.18 on 2023-04-19 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExtensionPackage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('version', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('zip', models.FileField(upload_to='extensions/')),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]
