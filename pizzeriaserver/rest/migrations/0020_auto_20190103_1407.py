# Generated by Django 2.1.2 on 2019-01-03 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0019_pizza_de_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='combos_promocionales',
            name='fecha_fin',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='combos_promocionales',
            name='fecha_inicio',
            field=models.DateField(auto_now_add=True),
        ),
    ]
