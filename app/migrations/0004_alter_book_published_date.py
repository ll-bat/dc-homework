# Generated by Django 4.1.2 on 2022-10-14 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_rename_published_data_book_published_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='published_date',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
