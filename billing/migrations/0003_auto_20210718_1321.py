# Generated by Django 3.1.5 on 2021-07-18 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0002_auto_20210718_1315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='counterhistory',
            name='service',
            field=models.CharField(choices=[('electricity_2_1', 'Электричество двухтарифный тариф 1'), ('electricity_2_2', 'Электричество двухтарифный тариф 2'), ('electricity_3_1', 'Электричество трехтарифный тариф 1'), ('electricity_3_2', 'Электричество трехтарифный тариф 2'), ('electricity_3_3', 'Электричество трехтарифный тариф 3'), ('water', 'Вода питьевая')], max_length=50, verbose_name='Услуга'),
        ),
        migrations.AlterField(
            model_name='tariff',
            name='service',
            field=models.CharField(choices=[('electricity_2_1', 'Электричество двухтарифный тариф 1'), ('electricity_2_2', 'Электричество двухтарифный тариф 2'), ('electricity_3_1', 'Электричество трехтарифный тариф 1'), ('electricity_3_2', 'Электричество трехтарифный тариф 2'), ('electricity_3_3', 'Электричество трехтарифный тариф 3'), ('water', 'Вода питьевая')], max_length=50, verbose_name='Услуга'),
        ),
    ]
