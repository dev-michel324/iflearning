from django.contrib import admin
from .models import tb_disciplines, tb_class, tb_modules, tb_dis_user


class DisciplinesAdmin(admin.ModelAdmin):
    list_display = ['dis_name']


class ModulesAdmin(admin.ModelAdmin):
    list_display = ['mod_name']


class ClassAdmin(admin.ModelAdmin):
    list_display = ['cla_name', 'cla_module']


admin.site.register(tb_disciplines, DisciplinesAdmin)
admin.site.register(tb_modules, ModulesAdmin)
admin.site.register(tb_class, ClassAdmin)
admin.site.register(tb_dis_user)
