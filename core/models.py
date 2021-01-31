from django.db import models
from django.contrib.auth.models import AbstractUser


class StroiUser(AbstractUser):
    phone = models.CharField("Телефон", max_length=20, null=True, blank=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class StroiPhone(models.Model):
    phone = models.CharField("Телефон", max_length=20, primary_key=True)
    description = models.CharField("Описание", max_length=300)

    class Meta:
        verbose_name = "Телефон владельца участка"
        verbose_name_plural = "Телефоны владельцев участков"
