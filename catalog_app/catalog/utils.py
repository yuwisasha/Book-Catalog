import requests
from json import loads as json_loads

from django.core.files.base import ContentFile
from django.db.models.query import QuerySet
from rest_framework.generics import get_object_or_404

from .serializers import ParseBookSerializer
from .models import Book, Category


def _download_and_save_image(book: Book) -> None:
    if book.thumbnail_url and not book.image:
        print(book.thumbnail_url)
        response = requests.get(book.thumbnail_url)
        image_name = book.thumbnail_url.split("/")[-1]
        book.image.save(image_name, ContentFile(response.content))


def _parse_books(url: str) -> None:
    resp = requests.get(url)
    resp_json = json_loads(resp.text)
    serializer = ParseBookSerializer(data=resp_json, many=True)

    if serializer.is_valid():
        serializer.save()
    else:
        print(serializer.errors)


def _traverse_category(categories_names: list[str]) -> Category:
    current_category = None

    for category_name in categories_names:
        if current_category:
            current_category = get_object_or_404(
                Category, title=category_name, parent=current_category
            )
        else:
            current_category = get_object_or_404(
                Category, title=category_name, parent=None
            )

    return current_category


def _get_category(category_path: str) -> Category:
    categories_names: list[str] = category_path.split("/")
    category: Category = _traverse_category(categories_names)

    return category


def _get_books_by_category(category: Category) -> QuerySet:

    return category.books


def _get_books_by_category_with_childs(category: Category) -> QuerySet:
    books: QuerySet = category.books.all()
    category_childrens: QuerySet = category.childs

    for category_ in category_childrens.all():
        books = books.union(category_.books.all())

    return books
