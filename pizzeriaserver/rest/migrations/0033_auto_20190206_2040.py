# Generated by Django 2.1.2 on 2019-02-06 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0032_auto_20190126_0742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='codigo',
            field=models.CharField(max_length=28, unique=True),
        ),
    ]
