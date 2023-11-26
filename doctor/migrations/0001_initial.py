# Generated by Django 4.2.7 on 2023-11-26 06:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Specialities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True)),
                ('slug', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Doctors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_image', models.ImageField(null=True, upload_to='images/doctors')),
                ('charge', models.PositiveIntegerField()),
                ('paypal_account', models.EmailField(max_length=70)),
                ('sun_start', models.TimeField(blank=True, null=True)),
                ('sun_end', models.TimeField(blank=True, null=True)),
                ('mon_start', models.TimeField(blank=True, null=True)),
                ('mon_end', models.TimeField(blank=True, null=True)),
                ('tue_start', models.TimeField(blank=True, null=True)),
                ('tue_end', models.TimeField(blank=True, null=True)),
                ('wed_start', models.TimeField(blank=True, null=True)),
                ('wed_end', models.TimeField(blank=True, null=True)),
                ('thu_start', models.TimeField(blank=True, null=True)),
                ('thu_end', models.TimeField(blank=True, null=True)),
                ('fri_start', models.TimeField(blank=True, null=True)),
                ('fri_end', models.TimeField(blank=True, null=True)),
                ('sat_start', models.TimeField(blank=True, null=True)),
                ('sat_end', models.TimeField(blank=True, null=True)),
                ('details', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='doctor', to=settings.AUTH_USER_MODEL)),
                ('specialized_in', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctor.specialities')),
            ],
        ),
    ]
