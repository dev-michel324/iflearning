from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from .models import tb_disciplines
from django.http import HttpResponse

from .forms import AddDiscipline


@login_required()
def index(request):
    return render(request, "disciplines/index.html")


@login_required()
def addDiscipline(request):
    if request.user.groups.filter(name='perm_to_crud_disciplines'):
        if request.method == 'POST':
            form = AddDiscipline(request.POST)
            if form.is_valid():
                name = form.cleaned_data['dis_name']
                discipline = tb_disciplines(
                    dis_name=name,
                    dis_user_created=request.user
                ).save()
                messages.success(request, "Disciplina adicionada.")
                return redirect("disciplines:disciplines-dashboard")
            return render(request, "disciplines/crud/disciplines/add.html", {'form': form})
        form = AddDiscipline()
        return render(request, "disciplines/crud/disciplines/add.html", {'form': form})
    messages.error(
        request, "Você não possui permissão para acessar essa página.")
    return redirect("disciplines:disciplines-dashboard")
