# Generated by Django 3.2 on 2021-07-20 07:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('analiz', '0014_remove_message_chat_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='event',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.CreateModel(
            name='ACOS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acos', models.DecimalField(decimal_places=0, max_digits=2)),
                ('spend', models.IntegerField()),
                ('sale', models.IntegerField()),
                ('budget', models.IntegerField()),
                ('product_name', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='analiz.typeofproduct')),
            ],
        ),
    ]