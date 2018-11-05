# Generated by Django 2.1.2 on 2018-10-30 21:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0009_tamano_borde_tamano_ingrediente_tamano_masa'),
    ]

    operations = [
        migrations.CreateModel(
            name='Combinacion_Adicional',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('adicional', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rest.Componente')),
            ],
        ),
        migrations.CreateModel(
            name='Combinacion_Pizza',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Combos_Promocionales',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
                ('costo', models.FloatField()),
                ('img_url', models.ImageField(upload_to='')),
                ('descripcion', models.TextField(blank=True, max_length=255)),
                ('fecha_inicio', models.DateTimeField(blank=True)),
                ('fecha_fin', models.DateTimeField(blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='combinacion_pizza',
            name='combo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rest.Combos_Promocionales'),
        ),
        migrations.AddField(
            model_name='combinacion_pizza',
            name='pizza',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rest.Pizza'),
        ),
        migrations.AddField(
            model_name='combinacion_pizza',
            name='tamano',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rest.Tamano'),
        ),
        migrations.AddField(
            model_name='combinacion_adicional',
            name='combo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rest.Combos_Promocionales'),
        ),
    ]