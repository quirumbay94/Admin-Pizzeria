# Generated by Django 2.1.2 on 2019-02-08 04:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0037_usuario_local'),
    ]

    operations = [
        migrations.CreateModel(
            name='Combinacion_Combo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('combinacion', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='rest.Combinacion')),
                ('combo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rest.Combos_Promocionales')),
            ],
        ),
    ]