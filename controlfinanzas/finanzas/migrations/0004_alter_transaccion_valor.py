# Generated by Django 4.2.13 on 2024-07-04 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0003_alter_transaccion_valor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaccion',
            name='valor',
            field=models.IntegerField(),
        ),
    ]
