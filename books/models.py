from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.contrib.auth import get_user_model


RUS_TO_LAT = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
    'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
    'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
    'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
    'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
}

def translit(text):
    text = text.lower()
    return ''.join(RUS_TO_LAT.get(ch, ch) for ch in text)


class Author(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    author_description = models.TextField(blank=True, null=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(translit(self.name))
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse("authorbyslug", kwargs={"author_slug": self.slug})


class Book(models.Model):
    title = models.CharField(max_length=300)
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books'
    )
    is_published = models.BooleanField(default=False)
    year = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    genre = models.ManyToManyField("genre", related_name='book')
    bookFile = models.FileField(upload_to='books/books_texts')
    book_avatar = models.ImageField(upload_to='books/books_avatars')
    posted_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='posted_by', null=True, blank=True)
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
    


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    
    def __str__(self):
        return self.name
    


