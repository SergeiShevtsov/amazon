# Generated by Django 3.2 on 2021-06-28 07:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('user', models.OneToOneField(default='1', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TypeOfProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=30, unique=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analiz.brand')),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analiz.manager')),
            ],
            options={
                'ordering': ['type'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=30)),
                ('asin', models.CharField(blank=True, max_length=15, null=True)),
                ('link', models.URLField(blank=True, null=True)),
                ('changes', models.TextField(blank=True, null=True)),
                ('positions_by_keys', models.CharField(blank=True, max_length=400, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=4)),
                ('bsr', models.IntegerField(blank=True, null=True)),
                ('sales', models.IntegerField()),
                ('conversion_rate', models.CharField(blank=True, max_length=10, null=True)),
                ('rating', models.DecimalField(decimal_places=1, max_digits=2)),
                ('offers', models.TextField(blank=True, null=True)),
                ('date', models.DateField()),
                ('event', models.TextField(blank=True, null=True)),
                ('reviews', models.IntegerField(blank=True, null=True)),
                ('link_to_seo', models.URLField(blank=True, null=True)),
                ('sel_acc', models.TextField(blank=True, null=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analiz.brand')),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analiz.manager')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analiz.typeofproduct')),
            ],
            options={
                'ordering': ['date'],
            },
        ),
    ]
