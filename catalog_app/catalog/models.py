from django.db import models


def book_image_path(instance: models.Model, filename: str) -> str:
    return "{0}/{1}".format(instance.title, filename)


class Author(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class Status(models.Model):
    title = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=255)
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="childs",
    )

    def __str__(self) -> str:
        return self.title


class Book(models.Model):
    title = models.TextField(null=True, blank=True)
    isbn = models.TextField(null=True, blank=True)
    page_count = models.IntegerField(null=True, blank=True)
    published_date = models.DateTimeField(null=True, blank=True)
    thumbnail_url = models.URLField(null=True, blank=True)
    short_description = models.TextField(null=True, blank=True)
    long_description = models.TextField(null=True, blank=True)
    status = models.ForeignKey(
        Status, on_delete=models.SET_NULL, null=True, blank=True
    )
    authors = models.ManyToManyField(Author, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="books",
    )
    image = models.ImageField(upload_to=book_image_path, null=True, blank=True)
