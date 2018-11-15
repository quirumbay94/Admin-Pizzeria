# Generated by Django 2.1.2 on 2018-11-12 05:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0011_auto_20181031_0529'),
    ]

    operations = [
        migrations.CreateModel(
            name='Combinacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=50)),
                ('fecha', models.DateField(auto_now_add=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Pizza_Tamano_Ingrediente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Porcion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
                ('valor', models.IntegerField()),
                ('estado', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Promocion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
                ('descripcion', models.CharField(max_length=255)),
                ('costo', models.FloatField(blank=True, default=0.0)),
                ('img_url', models.ImageField(upload_to='')),
                ('fecha_inicio', models.DateField(blank=True)),
                ('fecha_fin', models.DateField(blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='combinacion_adicional',
            name='combo',
        ),
        migrations.RemoveField(
            model_name='combinacion_pizza',
            name='combo',
        ),
        migrations.RemoveField(
            model_name='combinacion_pizza',
            name='tamano',
        ),
        migrations.AddField(
            model_name='pizza',
            name='tamano',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='rest.Tamano'),
        ),
        migrations.AlterField(
            model_name='pizza',
            name='borde',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rest.Tamano_Borde'),
        ),
        migrations.AlterField(
            model_name='pizza',
            name='descripcion',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='pizza',
            name='masa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rest.Tamano_Masa'),
        ),
        migrations.AddField(
            model_name='pizza_tamano_ingrediente',
            name='pizza',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rest.Pizza'),
        ),
        migrations.AddField(
            model_name='pizza_tamano_ingrediente',
            name='tamano_ingrediente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rest.Tamano_Ingrediente'),
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
        migrations.AddField(
            model_name='tamano_ingrediente',
            name='porcion',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='rest.Porcion'),
        ),
    ]