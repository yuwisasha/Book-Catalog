from rest_framework import serializers

from .models import Author, Category, Book, Status
from .fields import CustomDateTimeField, CustomListField


class StatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Status
        fields = "__all__"


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = (
            "title",
            "parent",
        )

    def get_parent(self, obj: Category):
        if obj.parent is not None:
            return CategorySerializer(obj.parent).data


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    status = StatusSerializer(read_only=True)

    class Meta:
        model = Book
        fields = (
            "title",
            "isbn",
            "page_count",
            "published_date",
            "thumbnail_url",
            "short_description",
            "long_description",
            "status",
            "authors",
            "category",
            "image",
        )


class ParseBookSerializer(serializers.Serializer):
    title = serializers.CharField(required=False)
    isbn = serializers.CharField(required=False)
    pageCount = serializers.IntegerField(required=False, source="page_count")
    publishedDate = CustomDateTimeField(
        required=False, source="published_date"
    )
    thumbnailUrl = serializers.URLField(required=False, source="thumbnail_url")
    shortDescription = serializers.CharField(
        required=False, source="short_description"
    )
    longDescription = serializers.CharField(
        required=False, source="long_description"
    )
    status = serializers.CharField(required=False)
    authors = CustomListField(
        child=serializers.CharField(allow_blank=True), required=False
    )
    categories = CustomListField(
        child=serializers.CharField(allow_blank=True), required=False
    )

    def create(self, validated_data: dict) -> Book:
        authors_data: list[str] = validated_data.pop("authors")
        categories_data: list[str] = validated_data.pop("categories")
        status_data: str = validated_data.pop("status")
        categories_depth = len(categories_data)

        status, created = Status.objects.get_or_create(title=status_data)

        book, created = Book.objects.get_or_create(
            status=status, **validated_data
        )

        for author_name in authors_data:
            author, created = Author.objects.get_or_create(name=author_name)
            book.authors.add(author)

        parent_category = None

        match categories_depth:
            case 0:
                parent_category, created = Category.objects.get_or_create(
                    title="Новинка", parent=None
                )
            case 1:
                parent_category, created = Category.objects.get_or_create(
                    title=categories_data[0], parent=None
                )
            case _:
                for category_title in categories_data:
                    category, careted = Category.objects.get_or_create(
                        title=category_title, parent=parent_category
                    )
                    parent_category = category

        parent_category.books.add(book)

        return book
