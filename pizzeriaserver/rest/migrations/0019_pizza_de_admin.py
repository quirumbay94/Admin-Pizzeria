# Generated by Django 2.1.2 on 2019-01-03 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0018_carrito_detallecarrito'),
    ]

    operations = [
        migrations.AddField(
            model_name='pizza',
            name='de_admin',
            field=models.BooleanField(default=False),
        ),
    ]
