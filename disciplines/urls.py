from django.urls import path

from . import views

app_name = "disciplines"

urlpatterns = [
    #crud displines
    path('', views.index, name="disciplines-dashboard"),
    path('add', views.addDiscipline, name="disciplines-add"),
    path('show/<int:id>', views.showDiscipline, name="showDiscipline"),
    path('edit/<int:discipline_id>', views.editDiscipline, name="discipline-edit"),
    path('remove/<int:discipline_id>', views.removeDiscipline, name='disciplines-remove'),
    # crud modules
    path('modules/add/<int:discipline_id>', views.addModule, name="addModule"),
    path('modules/edit/<int:discipline_id>/<int:module_id>', views.editModule, name="editModule"),
    path('modules/remove/<int:module_id>', views.removeModule, name="removeModule"),
    #crud class
    path('class/add/<int:discipline_id>/<int:module_id>', views.addClass, name="addClass"),
    path('class/show/<int:discipline_id>/<int:module_id>/<int:class_id>', views.showClass, name="showClass"),
    path('class/remove/<int:discipline_id>/<int:class_id>', views.removeClass, name="removeClass"),
    path('class/edit/<int:discipline_id>/<int:class_id>', views.editClass, name="editClass"),
]
