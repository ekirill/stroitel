from django.db import models
from django.contrib.auth.models import AbstractUser


class StroiUser(AbstractUser):
    REQUIRED_FIELDS = ['phone']
    phone = models.CharField("Телефон", max_length=20, null=True, blank=True, unique=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class StroiKnownPhone(models.Model):
    phone = models.CharField("Телефон", max_length=20, unique=True)
    description = models.CharField("Описание", max_length=300)

    def __str__(self):
        return f"{self.phone} [{self.description}]"

    class Meta:
        verbose_name = "Телефон владельца участка"
        verbose_name_plural = "Телефоны владельцев участков"
