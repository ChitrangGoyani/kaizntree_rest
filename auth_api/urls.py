from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('forgotPassword/', views.forgotpassword, name='forgotpass'),
    path('logout/', views.logout, name='logout')
]