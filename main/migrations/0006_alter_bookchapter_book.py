# Generated by Django 4.1.2 on 2022-10-31 10:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_bookinfo_bookimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookchapter',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_chapters', to='main.bookinfo'),
        ),
    ]
