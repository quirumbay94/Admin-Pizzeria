# Generated by Django 2.1.2 on 2019-01-15 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0024_auto_20190115_1348'),
    ]

    operations = [
        migrations.AddField(
            model_name='local',
            name='img_url',
            field=models.ImageField(default=None, upload_to=''),
        ),
    ]