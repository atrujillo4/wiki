from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("wiki/<str:title>", views.page, name="page"),
    path("wiki/<str:title>/edit", views.edit, name="edit"),
    path("search", views.search, name="search"),
    path("random_page", views.random_page, name="random_page")
]
