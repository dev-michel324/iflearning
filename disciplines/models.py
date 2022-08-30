from django.db import models
from accounts.models import CustomUser


class tb_disciplines(models.Model):
    dis_name = models.CharField(max_length=255, unique=True, null=False)
    dis_user_created = models.ForeignKey(
        CustomUser, related_name="user_dis_created", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.dis_name


class tb_dis_user(models.Model):
    dis_discipline = models.ForeignKey(
        tb_disciplines, related_name="discipine", on_delete=models.CASCADE)
    dis_user = models.ForeignKey(
        CustomUser, related_name="user_dis", on_delete=models.CASCADE)

    def __str__(self):
        return self.dis_user.username


class tb_modules(models.Model):
    mod_name = models.CharField(max_length=155, null=False)
    mod_discipline = models.ForeignKey(
        tb_disciplines, related_name="mod_discipline", on_delete=models.CASCADE, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.mod_name


class tb_class(models.Model):
    cla_name = models.CharField(max_length=255, null=False)
    cla_videourl = models.URLField(null=False)
    cla_module = models.ForeignKey(
        tb_modules, related_name="cla_module", null=False, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.cla_name
