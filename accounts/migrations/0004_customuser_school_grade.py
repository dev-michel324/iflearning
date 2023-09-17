# Generated by Django 4.1.2 on 2023-09-17 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_remove_customuser_school_grade'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='school_grade',
            field=models.CharField(choices=[('Ensino Fundamental', 'Ensino Fundamental'), ('Ensino Médio', 'Ensino Médio'), ('Ensino Superior', 'Ensino Superior')], default='Ensino Médio', max_length=19),
        ),
    ]
