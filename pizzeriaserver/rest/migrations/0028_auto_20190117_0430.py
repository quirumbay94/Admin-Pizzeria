# Generated by Django 2.1.2 on 2019-01-17 04:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0027_auto_20190117_0419'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poligono',
            name='local',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='rest.Local', unique=True),
        ),
    ]