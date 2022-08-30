from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from accounts.models import CustomUser
from .forms import UserLoginModelForm, UserRegisterModelForm

from disciplines.models import tb_disciplines, tb_dis_user


def index(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    return render(request, 'accounts/index.html')


@login_required(login_url='/login')
def dashboard(request):
    disciplines = tb_disciplines.objects.all().exclude(
        discipine__dis_user_id=request.user.id)
    myDisciplines = tb_dis_user.objects.filter(dis_user=request.user.id)
    if request.user.groups.filter(name='perm_to_crud_disciplines'):
        return render(request, "accounts/dashboard.html", {'disciplines': disciplines, 'my_disciplines': myDisciplines, 'has_perm_crud_disciplines': True})
    return render(request, "accounts/dashboard.html", {'disciplines': disciplines, 'my_disciplines': myDisciplines, 'has_perm_crud_disciplines': False})


@login_required(login_url="/login")
def addDisciplineToUser(request, id):
    discipline = get_object_or_404(tb_disciplines, pk=id)
    disciplineUserExists = tb_dis_user.objects.filter(
        dis_discipline=discipline, dis_user=request.user)
    if not disciplineUserExists.exists():
        tb_dis_user(
            dis_discipline=discipline,
            dis_user=request.user
        ).save()
        messages.success(request, "Disciplina adicionada.")
        return redirect('accounts:dashboard')
    messages.error(request, "Você já possui essa disciplina.")
    return redirect('accounts:dashboard')


def userLogin(request):
    if request.user.is_authenticated:
        return redirect("accounts:dashboard")
    form = UserLoginModelForm()
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('accounts:dashboard')
        else:
            messages.error(request, "Email ou senha inválidos")
    return render(request, "accounts/auth/login.html", {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserRegisterModelForm(request.POST)
        if form.is_valid():
            user = CustomUser(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['firstname'],
                last_name=form.cleaned_data['lastname'],
                birth=form.cleaned_data['birth'],
            )
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Usuário cadastrado com sucesso!")
            return redirect('accounts:login')
        return render(request, "accounts/auth/register.html", {'form': form})
    form = UserRegisterModelForm()
    return render(request, "accounts/auth/register.html", {'form': form})


def userLogout(request):
    if request.user.is_authenticated:
        messages.success(request, "Você saiu!")
        logout(request)
    return redirect("accounts:home")
