# Generated by Django 3.2 on 2021-07-02 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analiz', '0006_typeofproduct_ostatki'),
    ]

    operations = [
        migrations.AddField(
            model_name='typeofproduct',
            name='owner',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]
