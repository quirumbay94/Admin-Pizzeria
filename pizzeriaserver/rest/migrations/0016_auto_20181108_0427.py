# Generated by Django 2.1.2 on 2018-11-08 04:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0015_auto_20181108_0424'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='combinacion_adicional',
            name='combo',
        ),
        migrations.RemoveField(
            model_name='combinacion_pizza',
            name='combo',
        ),
        migrations.AddField(
            model_name='combinacion_adicional',
            name='combinacion',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='rest.Combinacion'),
        ),
        migrations.AddField(
            model_name='combinacion_pizza',
            name='combinacion',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='rest.Combinacion'),
        ),
        migrations.AddField(
            model_name='combos_promocionales',
            name='combinacion',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='rest.Combinacion'),
        ),
    ]
