from django.urls import path

from .views import CreateUserView


urlpatterns = [
    path("sign_up/", CreateUserView.as_view()),
]
