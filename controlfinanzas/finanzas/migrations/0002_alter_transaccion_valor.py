# Generated by Django 4.2.13 on 2024-06-27 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaccion',
            name='valor',
            field=models.DecimalField(decimal_places=3, max_digits=10),
        ),
    ]
