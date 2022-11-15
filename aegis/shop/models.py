from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from .managers import CustomUserManager


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(gettext_lazy('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'

    """
    def save(self, *args, **kwargs):
        o = Orders()
        o.account = self.pk
        o.save()
        super().save(*args, **kwargs)
    """

class Сategories(models.Model):
    name = models.CharField('Наименоние', max_length=25)
    slug = models.SlugField(max_length=50, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']


class Kinds(models.Model):
    name = models.CharField('Наименоние', max_length=50)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('kind', kwargs={'kind_id': self.pk})

    class Meta:
        verbose_name = 'Вид'
        verbose_name_plural = 'Виды'


class Products(models.Model):
    slug = models.SlugField(max_length=50, unique=True, db_index=True, verbose_name="URL")
    cat = models.ForeignKey('Сategories', on_delete=models.SET_NULL, null=True, verbose_name="Категория")
    kind = models.ForeignKey('Kinds', on_delete=models.SET_NULL, null=True, verbose_name="Вид")
    year = models.DateField(verbose_name="Дата появления")
    photo = models.ImageField('Фото формы', upload_to='main/img/ShopAE')
    price = models.DecimalField('Цена', max_digits=7, decimal_places=2)

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('product', kwargs={'product_slug': self.slug})

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['id']


class Orders(models.Model):
    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    account = models.ForeignKey('Account', on_delete=models.SET_NULL, null=True, verbose_name="Пользователь")
    dataTime = models.DateTimeField('Дата и время заказа', null=True)
    phone_number = models.CharField('Номер телефона', validators=[phoneNumberRegex], null=True, max_length=16)
    sum_price = models.DecimalField('Сумма заказа', max_digits=10, null=True, decimal_places=2)
    status = models.BooleanField('Завершена ли покупка?', null=True)

    def __str__(self):
        return self.account

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class Purchases(models.Model):
    order = models.ForeignKey('Orders', on_delete=models.SET_NULL, null=True, verbose_name="Карзина")
    product = models.ForeignKey('Products', on_delete=models.SET_NULL, null=True, verbose_name="Товар")
    size = models.CharField(verbose_name="Размер", max_length=4)
    quantity = models.PositiveSmallIntegerField(verbose_name="Количество")

    def __str__(self):
        return self.product

    class Meta:
        verbose_name = 'Товар из корзины'
        verbose_name_plural = 'Товары из корзины'
