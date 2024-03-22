from django.urls import path

from .views import (
    ListBookView,
    ListBookByCategoryView,
    ListBookByCategoryAndChildsView,
    RetrieveBookView,
)


urlpatterns = [
    path("<str:title>/", RetrieveBookView.as_view()),
    path("", ListBookView.as_view()),
    path(
        "2-level/<path:category_path>/",
        ListBookByCategoryAndChildsView.as_view(),
    ),
    path("<path:category_path>/", ListBookByCategoryView.as_view()),
]
