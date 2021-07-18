# Generated by Django 3.1.5 on 2021-07-18 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='counter',
            name='service_type',
            field=models.CharField(choices=[('electricity_2_tariff', 'Электричество двухтарифный'), ('electricity_3_tariff', 'Электричество трехтарифный'), ('water', 'Вода питьевая')], max_length=50, verbose_name='Тип услуги'),
        ),
    ]
