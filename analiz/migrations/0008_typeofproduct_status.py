# Generated by Django 3.2 on 2021-07-12 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analiz', '0007_typeofproduct_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='typeofproduct',
            name='status',
            field=models.CharField(choices=[('InDev', 'В разработке'), ('IsS', 'Продается'), ('NotS', 'Не продается')], default='IsS', max_length=20),
        ),
    ]