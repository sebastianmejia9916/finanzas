# Generated by Django 4.2.13 on 2024-07-04 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0004_alter_transaccion_valor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaccion',
            name='valor',
            field=models.DecimalField(decimal_places=3, max_digits=13),
        ),
    ]
