# Generated by Django 4.2.1 on 2023-05-13 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_remove_like_post_remove_like_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='posts',
            field=models.ManyToManyField(related_name='profiles', to='blog.post'),
        ),
    ]