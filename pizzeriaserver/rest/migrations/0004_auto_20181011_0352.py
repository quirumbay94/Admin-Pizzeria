# Generated by Django 2.0.8 on 2018-10-11 03:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0003_auto_20181011_0235'),
    ]

    operations = [
        migrations.CreateModel(
            name='Borde',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=255)),
                ('estado', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Masa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=255)),
                ('estado', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pizza',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=255)),
                ('img_url', models.ImageField(blank=True, upload_to='')),
                ('estado', models.BooleanField(default=True)),
                ('borde', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rest.Borde')),
                ('masa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rest.Masa')),
            ],
        ),
        migrations.CreateModel(
            name='Pizza_Tradicional',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('costo', models.FloatField()),
                ('estado', models.BooleanField(default=True)),
                ('pizza', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rest.Pizza')),
            ],
        ),
        migrations.AlterField(
            model_name='componente',
            name='estado',
            field=models.BooleanField(default=True),
        ),
    ]
