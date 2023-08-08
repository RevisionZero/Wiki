from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.display_entry, name="displayEntry"),
    path("search", views.search, name="search"),
    path("wiki", views.index, name="wiki"),
    path("create-entry", views.create_entry, name="create"),
    path("wiki/<str:name>/edit", views.edit_entry, name="edit")
]
