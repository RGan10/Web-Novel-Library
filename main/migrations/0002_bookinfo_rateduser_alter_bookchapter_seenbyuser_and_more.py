# Generated by Django 4.1.2 on 2022-10-26 15:57

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookinfo',
            name='ratedUser',
            field=models.ManyToManyField(related_name='list_of_Rated_Users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='bookchapter',
            name='seenByUser',
            field=models.ManyToManyField(related_name='list_of_Users_that_have_seen_chapter', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='bookinfo',
            name='bookUsers',
            field=models.ManyToManyField(related_name='list_of_Book_Users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='bookinfo',
            name='userRating',
            field=models.PositiveIntegerField(),
        ),
    ]