from django.contrib import admin
from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path('', views.index, name="home"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('login', views.userLogin, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.userLogout, name='logout'),
    path('addDisciplineToUser/<int:id>', views.addDisciplineToUser,
         name="add-discipline-to-user")
]
