from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


# Create your models here.

class Book(models.Model):
    isbn = models.CharField(max_length=13, db_index=True, blank=False, null=False, validators=[MinValueValidator(1)])
    title = models.CharField(max_length=512, blank=False, null=False, validators=[MinValueValidator(1)])
    description = models.TextField(blank=True, null=True)

    authors = models.JSONField(blank=True, null=True)
    publisher = models.CharField(max_length=256, blank=True, null=True)
    published_date = models.CharField(max_length=15, blank=True, null=True)
    page_count = models.SmallIntegerField(blank=True, null=True)
    categories = models.JSONField(blank=True, null=True)
    image_links = models.JSONField(blank=True, null=True)
    language = models.CharField(max_length=10, blank=True, null=True)
    preview_link = models.CharField(max_length=512, blank=True, null=True)
    info_link = models.CharField(max_length=512, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,
                                   on_delete=models.DO_NOTHING,
                                   related_name='created_by_books',
                                   db_column='created_by')

    updated_by = models.ForeignKey(User,
                                   on_delete=models.DO_NOTHING,
                                   related_name='updated_by_books',
                                   db_column='updated_by')

    class Meta:
        db_table = "books"
