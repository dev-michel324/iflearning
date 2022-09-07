from email import message
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect

import disciplines
from .models import tb_disciplines, tb_modules
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404

from .forms import *
from .models import tb_dis_user

@login_required()
def index(request):
    return render(request, "disciplines/index.html")


@login_required()
def addDiscipline(request):
    if not verifyIfUserHasPermission(request):
        return redirect('accounts:dashboard')
    if request.method == 'POST':
        form = AddDiscipline(request.POST)
        if form.is_valid():
            name = form.cleaned_data['dis_name']
            discipline = tb_disciplines(
                dis_name=name,
                dis_user_created=request.user
            ).save()
            messages.success(request, "Disciplina adicionada.")
            return redirect("accounts:dashboard")
        return render(request, "disciplines/crud/disciplines/add.html", {'form': form})
    form = AddDiscipline()
    return render(request, "disciplines/crud/disciplines/add.html", {'form': form})

@login_required()
def showDiscipline(request, id):
    myDiscipline = tb_disciplines.objects.filter(id=id, discipine__dis_user=request.user.id)[:1]
    if not myDiscipline:
        messages.error(request, "Você não possui a disciplina acessada.")
        return redirect("accounts:dashboard")
    disciplineModules = tb_modules.objects.filter(mod_discipline=id)
    if request.user.groups.filter(name='perm_to_crud_disciplines'):
        return render(request, "disciplines/crud/disciplines/show.html", {'my_discipline': myDiscipline[0], 'modules': disciplineModules, 'has_perm_crud': True})
    return render(request, "disciplines/crud/disciplines/show.html", {'my_discipline': myDiscipline[0], 'modules': disciplineModules})

@login_required()
def removeDiscipline(request, discipline_id):
    if not verifyIfUserIsOwnerOfDiscipline(request, discipline_id):
        return redirect('accounts:dashboard')
    if request.method == 'POST':
        discipline = get_object_or_404(tb_disciplines, pk=discipline_id)
        discipline.delete()
        messages.success(request, 'Disciplina removida com sucesso.')
        return redirect('accounts:dashboard')
    messages.error(request, 'Essa disciplina não ou existe, ou então, não pertence a você.')
    return redirect('accounts:dashboard')

@login_required()
def editDiscipline(request, discipline_id):
    if not verifyIfUserHasPermission(request):
        return redirect('accounts:dashboard')
    if not verifyIfUserIsOwnerOfDiscipline(request, discipline_id):
        return redirect('accounts:dashboard')
    discipline = get_object_or_404(tb_disciplines, pk=discipline_id)
    if request.method == 'POST':
        form = AddDiscipline(request.POST)
        if form.is_valid():
            discipline.dis_name = form.cleaned_data['dis_name']
            discipline.save()
            messages.success(request, 'Disciplina atualizada com sucesso!')
            return redirect('accounts:dashboard')
    form = AddDiscipline(instance=discipline)
    return render(request, 'disciplines/crud/disciplines/edit.html', {'form': form})

@login_required()
def addModule(request, discipline_id):
    if not verifyIfUserHasPermission(request):
        return redirect('accounts:dashboard')
    if not verifyIfUserIsOwnerOfDiscipline(request, discipline_id):
        return redirect('accounts:dashboard')
    if request.method == 'POST':
        form = AddModule(request.POST)
        if form.is_valid():
            discipline = get_object_or_404(tb_disciplines, pk=discipline_id)
            module = tb_modules(
                mod_name = form.cleaned_data['mod_name'],
                mod_discipline = discipline
            ).save()
            messages.success(request, 'Modulo adicionado com sucesso.')
            return redirect('disciplines:showDiscipline', id=discipline_id)
        messages.error(request, 'Dados inválidos')
        return render(request, 'disciplines/crud/modules/add.html', {'form': form})
    form = AddModule()
    return render(request, 'disciplines/crud/modules/add.html', {'form': form})

@login_required()
def editModule(request, discipline_id, module_id):
    if not verifyIfUserHasPermission(request):
        return redirect('accounts:dashboard')
    if not verifyIfUserIsOwnerOfDiscipline(request, discipline_id):
        return redirect('accounts:dashboard')
    module = tb_modules.objects.filter(id=module_id)
    if module.exists():
        module = module[0]
        if module.mod_discipline.id == discipline_id:
            if request.method == "POST":
                form = AddModule(request.POST)
                if form.is_valid():
                    module = tb_modules.objects.get(id=module_id)
                    module.mod_name = form.cleaned_data['mod_name']
                    module.save()
                    messages.success(request, 'Modulo editado com sucesso.')
                    return redirect('disciplines:showDiscipline', id=discipline_id)
            form = AddModule(instance=module)
            return render(request, 'disciplines/crud/modules/edit.html', {'form': form})
        messages.error(request, 'Esse modulo não existe na disciplina.')
        return redirect('accounts:dashboard')
    messages.error(request, 'Esse modulo não existe.')
    return redirect('accounts:dashboard')

@login_required()
def removeModule(request, module_id):
    if not verifyIfUserHasPermission(request):
        return redirect('accounts:dashboard')
    if request.method == 'POST':
        module = tb_modules.objects.filter(id=module_id, mod_discipline__dis_user_created_id=request.user.id)
        print(module)
        module = get_object_or_404(tb_modules, pk=module_id)
        module.delete()
        messages.success(request, "Modulo removido com sucesso.")
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required()
def addClass(request, module_id, discipline_id):
    if not verifyIfUserHasPermission(request):
        return redirect('accounts:dashboard')
    if not verifyIfModuleExist(request, module_id, discipline_id):
        return redirect('accounts:dashboard')
    if request.method == 'POST':
        form = AddClass(request.POST)
        if form.is_valid():
            module = get_object_or_404(tb_modules, pk=module_id)
            class_added = tb_class(
                cla_name= form.cleaned_data['cla_name'],
                cla_videourl = form.cleaned_data['cla_videourl']
            ).save()
            class_added = tb_class.objects.get(cla_videourl=form.cleaned_data['cla_videourl'])
            print(class_added)
            module.mod_classes.add(class_added)
            messages.success(request, 'Aula adicionada com sucesso!')
            return redirect('disciplines:showDiscipline', id=discipline_id)
        return render(request, 'disciplines/crud/class/add.html', {'form': form})
    form = AddClass()
    return render(request, 'disciplines/crud/class/add.html', {'form': form})

@login_required()
def editClass(request, discipline_id, class_id):
    if not verifyIfUserHasPermission(request):
        return redirect('accounts:dashboard')
    if not verifyIfUserIsOwnerOfDiscipline(request, discipline_id):
        return redirect('accounts:dashboard')
    class_obj = get_object_or_404(tb_class, pk=class_id)
    if request.method == 'POST':
        form = AddClass(request.POST)
        if form.is_valid():
            class_obj.cla_name = form.cleaned_data['cla_name']
            class_obj.cla_videourl = form.cleaned_data['cla_videourl']
            class_obj.save()
            messages.success(request, 'Aula atualizada com sucesso.')
            return redirect('disciplines:showDiscipline', id=discipline_id)
    form = AddClass(instance=class_obj)
    return render(request, 'disciplines/crud/class/edit.html', {'form': form})

@login_required()
def removeClass(request, discipline_id, class_id):
    if not verifyIfUserHasPermission(request):
        return redirect('accounts:dashboard')
    if not verifyIfUserIsOwnerOfDiscipline(request, discipline_id):
        return redirect('accounts:dashboard')
    class_obj = get_object_or_404(tb_class, pk=class_id)
    class_obj.delete()
    messages.success(request, 'Aula removida com sucesso.')
    return redirect('disciplines:showDiscipline', id=discipline_id)

@login_required()
def showClass(request, discipline_id, module_id, class_id):
    if not verifyIfUserHasDiscipline(request, discipline_id):
        return redirect('accounts:dashboard')
    class_obj = get_object_or_404(tb_class, pk=class_id)
    class_videourl = str(class_obj.cla_videourl).replace('watch?v=', 'embed/')
    return render(request, 'disciplines/crud/class/show.html', {'class': class_obj, 'videourl': class_videourl})

def verifyIfModuleExist(request, module_id, discipline_id):
    if not verifyIfUserIsOwnerOfDiscipline(request, discipline_id):
        if not tb_modules.objects.filter(id=module_id).exists():
            messages.error(request, 'Esse modulo não existe na disciplina.')
            return False
        return False
    return True

def verifyIfUserHasDiscipline(request, discipline_id):
    discipline = tb_dis_user.objects.filter(dis_discipline=discipline_id, dis_user=request.user.id)
    if not discipline:
        messages.error(request, 'A disciplina que contém a aula não existe')
        return False
    return True

def verifyIfUserHasPermission(request):
    if not request.user.groups.filter(name='perm_to_crud_disciplines'):
        messages.error(request, 'Você não possui permissão para esta ação.')
        return False
    return True

def verifyIfUserIsOwnerOfDiscipline(request, discipline_id):
    discipline = tb_disciplines.objects.filter(id=discipline_id, dis_user_created=request.user.id)
    if not discipline.exists():
        messages.error(request, 'A disciplina não existe, ou então você não é o dono dessa disciplina.')
        return False
    return True