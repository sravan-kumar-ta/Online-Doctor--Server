# Generated by Django 4.2.7 on 2023-11-27 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='is_public',
            field=models.BooleanField(default=False),
        ),
    ]
