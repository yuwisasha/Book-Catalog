from typing import Any
from django.contrib import admin

from .models import Book, Category


class BookAdmin(admin.ModelAdmin):
    fields = [field.name for field in Book._meta.fields if field.name != "id"]
    search_fields = ("title",)
    list_display = ("title", "isbn")
    date_hierarchy = "published_date"


class RootObjectFilter(admin.SimpleListFilter):
    title = "Root Objects"
    parameter_name = "is_root"

    def lookups(self, request, model_admin):
        return (
            ("yes", "Yes"),
            ("no", "No"),
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(parent=None)
        elif self.value() == "no":
            return queryset.exclude(parent=None)


class CategoryInlineAdmin(admin.StackedInline):
    model = Category
    extra = 1
    show_change_link = True


class CategoryAdmin(admin.ModelAdmin):
    fields = ("title",)
    search_fields = ("title",)
    inlines = [
        CategoryInlineAdmin,
    ]
    list_filter = (RootObjectFilter,)


admin.site.register(Book, BookAdmin)
admin.site.register(Category, CategoryAdmin)
