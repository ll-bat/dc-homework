# Generated by Django 4.1.2 on 2022-10-13 19:08

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_book_authors_alter_book_categories_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='published_data',
            new_name='published_date',
        ),
        migrations.AddField(
            model_name='book',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='isbn',
            field=models.CharField(db_index=True, max_length=13, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=512, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
