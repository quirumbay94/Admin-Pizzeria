# Generated by Django 2.0.8 on 2018-10-11 02:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0002_componente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='componente',
            name='estado',
            field=models.BooleanField(),
        ),
    ]
