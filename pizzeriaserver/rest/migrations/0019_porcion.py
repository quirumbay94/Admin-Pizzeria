# Generated by Django 2.1.2 on 2018-11-08 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0018_auto_20181108_1600'),
    ]

    operations = [
        migrations.CreateModel(
            name='Porcion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
                ('valor', models.IntegerField()),
                ('estado', models.BooleanField(default=True)),
            ],
        ),
    ]
