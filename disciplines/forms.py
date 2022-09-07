from django import forms
from .models import tb_class, tb_disciplines, tb_modules


class AddDiscipline(forms.ModelForm):
    class Meta:
        model = tb_disciplines
        fields = ['dis_name']

    dis_name = forms.CharField(
        label="Nome",
        required=True
    )

class AddModule(forms.ModelForm):
    class Meta:
        model = tb_modules
        fields = ['mod_name']

    mod_name = forms.CharField(
        label="Nome do Modulo",
        required=True,
    )

class AddClass(forms.ModelForm):
    class Meta:
        model = tb_class
        fields = ['cla_name', 'cla_videourl']

    cla_name = forms.CharField(
        label="Titulo da aula",
        required=True
    )
    cla_videourl = forms.URLField(
        label="Link da aula",
        required=True
    )