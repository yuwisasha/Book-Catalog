from django.contrib import admin
from .models import Contact


@admin.display(description="Message")
def message_first_words(obj):
    return f"{obj.message[:40]}"


class ContactAdmin(admin.ModelAdmin):
    fields = (
        ("email", "phone"),
        "name",
        "message",
    )
    list_display = ("email", message_first_words)


admin.site.register(Contact, ContactAdmin)
