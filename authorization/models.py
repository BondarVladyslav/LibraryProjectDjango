from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE , related_name='additional_data')
    favourite_books = models.ManyToManyField('books.Book', related_name='favourite_books', blank=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username