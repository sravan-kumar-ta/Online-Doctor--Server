# Generated by Django 4.2.7 on 2023-11-27 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_posts_is_public'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='image',
            field=models.ImageField(default='static/img/blog.jpg', upload_to='user_uploads/blogs'),
        ),
    ]