from django.db import models
from django.utils.timezone import now


SERVICE_ELECTRICITY_1 = 'electricity_1'
SERVICE_ELECTRICITY_2 = 'electricity_2'
SERVICE_ELECTRICITY_3 = 'electricity_3'
SERVICE_WATER = 'water'

SERVICE_TYPE_ELECTRICITY = "electricity"
SERVICE_TYPE_WATER = "water"

SERVICE_CHOICES = (
    (SERVICE_ELECTRICITY_1, "Электричество (тариф 1)"),
    (SERVICE_ELECTRICITY_2, "Электричество (тариф 2)"),
    (SERVICE_ELECTRICITY_3, "Электричество (тариф 3)"),
    (SERVICE_WATER, "Вода питьевая"),
)

SERVICE_TYPE_CHOICES = (
    (SERVICE_TYPE_ELECTRICITY, "Электричество"),
    (SERVICE_TYPE_WATER, "Вода питьевая"),
)

SERVICES_BY_TYPE = {
    SERVICE_TYPE_ELECTRICITY: (
        SERVICE_ELECTRICITY_1,
        SERVICE_ELECTRICITY_2,
        SERVICE_ELECTRICITY_3,
    ),
    SERVICE_TYPE_WATER: (
        SERVICE_WATER,
    )
}

SERVICE_TYPE_BY_SERVICE = {}
for t, s in SERVICES_BY_TYPE.items():
    SERVICE_TYPE_BY_SERVICE[s] = t


class Tariff(models.Model):
    service = models.CharField("Услуга", max_length=50, choices=SERVICE_CHOICES)
    start_date = models.DateField("Начало действия", default=now)
    end_date = models.DateField("Окончание действия", null=True, blank=True)
    price = models.DecimalField("Цена", max_digits=5, decimal_places=2)

    class Meta:
        unique_together = ("service", "start_date")
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"

    def __str__(self):
        return f"Тариф {self.get_service_display()} [{self.start_date}-{self.end_date or ''}]"


class Counter(models.Model):
    house = models.CharField("Участок", max_length=50)
    description = models.CharField("Описание", max_length=300, blank=True)
    serial = models.CharField("Серийный номер", max_length=100, blank=True)
    service_type = models.CharField("Тип услуги", max_length=50, choices=SERVICE_TYPE_CHOICES)

    class Meta:
        verbose_name = "Счетчик"
        verbose_name_plural = "Счетчики"

    def __str__(self):
        return f"Счетчик уч {self.house}[{self.get_service_type_display()}]"


class CounterHistory(models.Model):
    counter = models.ForeignKey(Counter, verbose_name="Счетчик", on_delete=models.PROTECT)
    service = models.CharField("Услуга", max_length=50, choices=SERVICE_CHOICES)
    date = models.DateField("Дата")
    value = models.IntegerField("Показание")

    class Meta:
        verbose_name = "Показание"
        verbose_name_plural = "Показания"

    def __str__(self):
        return f"{self.date} {self.get_service_display()}: {self.value}"
