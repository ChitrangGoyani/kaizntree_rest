from django.urls import path
from . import views

urlpatterns = [
    path('', views.getItems, name='get_all'),
    path('add/', views.addItem, name='add_item'),
    path('item/', views.getItem, name='get_item'),
    path('delete/', views.deleteItem, name='delete_item'),
    path('update/', views.updateItem, name='updated_item'),
    path('filter/', views.filterItems, name='filters')
]
