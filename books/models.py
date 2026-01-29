from django.db import models


# Author -> full_name,birth_date, bio
# book -> title, description, published_date, page, genre
#
# one to many
#
# author create  table query
# book create table ref_id author_id fk ni boglab ketamiz
# tableni yaratish

class Author(models.Model):
    full_name = models.CharField(max_length=255)
    birth_date = models.DateTimeField(null=True, blank=True)
    bio = models.TextField()

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'authors'


class Genre(models.TextChoices):
    BADIIY = 'badiiy', 'Badiiy'
    ILMIY = 'ilmiy', 'Ilmiy'


class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    page_count = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=6,
                                decimal_places=2)  # 6 xonali raqam . dan keyin 2 ta son bolishi mumkin 1222.22
    genre = models.CharField(max_length=50, choices=Genre, default=Genre.BADIIY)
    published_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'books'

