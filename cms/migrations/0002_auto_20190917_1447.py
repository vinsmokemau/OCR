# Generated by Django 2.2.4 on 2019-09-17 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='excel',
            field=models.FileField(blank=True, upload_to='excels', verbose_name='excel'),
        ),
    ]
