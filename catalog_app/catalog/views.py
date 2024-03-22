from rest_framework.generics import ListAPIView, RetrieveAPIView
from django.db.models.query import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .serializers import BookSerializer
from .paginators import CatalogPagintaion
from .models import Book
from .utils import (
    _get_books_by_category,
    _get_books_by_category_with_childs,
    _get_category,
)


class RetrieveBookView(RetrieveAPIView):

    serializer_class = BookSerializer
    queryset = Book.objects
    lookup_field = "title"


class ListBookView(ListAPIView):

    serializer_class = BookSerializer
    pagination_class = CatalogPagintaion
    queryset = Book.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ("title",)
    filterset_fields = {
        "published_date": ["gte", "lte"],
        "status": ("exact",),
        "authors": ("exact",),
    }
    ordering_fields = ("published_date",)


class ListBookByCategoryView(ListAPIView):

    serializer_class = BookSerializer
    pagination_class = CatalogPagintaion

    def get_queryset(self) -> QuerySet:
        category_path: str = self.kwargs.get("category_path")
        category = _get_category(category_path)

        return _get_books_by_category(category).all()


class ListBookByCategoryAndChildsView(ListAPIView):

    serializer_class = BookSerializer
    pagination_class = CatalogPagintaion

    def get_queryset(self):
        category_path: str = self.kwargs.get("category_path")
        category = _get_category(category_path)

        return _get_books_by_category_with_childs(category).all()
