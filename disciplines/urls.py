from django.urls import path

from . import views

app_name = "disciplines"

urlpatterns = [
    path('', views.index, name="disciplines-dashboard"),
    path('/add', views.addDiscipline, name="disciplines-add")
]
