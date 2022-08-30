from django import forms
from .models import tb_disciplines


class AddDiscipline(forms.ModelForm):
    class Meta:
        model = tb_disciplines
        fields = ['dis_name']

    dis_name = forms.CharField(
        label="Nome",
        required=True
    )
