# Generated by Django 4.1 on 2022-09-07 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('disciplines', '0002_remove_tb_class_cla_module_tb_modules_mod_classes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tb_class',
            name='cla_videourl',
            field=models.URLField(unique=True),
        ),
    ]