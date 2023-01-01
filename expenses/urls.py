from django.urls import path
from . import views

urlpatterns = [

    path("", views.index, name="expenses"),
    path("add-expense", views.add_expense, name="add-expenses"),
    path("update-expense/<int:id>", views.update_expense, name="update-expense"),
    path("delete-expense/<int:id>", views.delete_expense, name="delete-expense"),
]
