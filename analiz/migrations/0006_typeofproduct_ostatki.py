# Generated by Django 3.2 on 2021-07-01 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analiz', '0005_auto_20210628_1321'),
    ]

    operations = [
        migrations.AddField(
            model_name='typeofproduct',
            name='ostatki',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]