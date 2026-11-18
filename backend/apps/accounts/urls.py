from django.urls import path

from .views import RegistroView

app_name = "accounts"

urlpatterns = [
    path("registro/", RegistroView.as_view(), name="registro"),
]