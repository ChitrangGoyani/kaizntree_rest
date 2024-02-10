from django.urls import path
from . import views

urlpatterns = [
    path('', views.getItems),
    path('add/', views.addItem),
    path('item/', views.getItem),
    path('delete/', views.deleteItem),
    path('filter/', views.filterItems)
]
