from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name = "wiki"),
    path("search", views.search, name="search"),
    path("create", views.create, name="create"), # returns the html page to create a new entry
    path("create_entry", views.create_entry, name="create_entry") # creates a new entry and returns that page
]
