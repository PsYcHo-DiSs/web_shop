from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

from .utils import unique_category_image_path, unique_gallery_image_path


class Category(models.Model):
    """Модель категории товаров"""

    title = models.CharField(max_length=150, verbose_name='Наименование категории')
    image = models.ImageField(upload_to=unique_category_image_path, null=True, blank=True, verbose_name='Изображение')
    slug = models.SlugField(unique=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                               verbose_name='Категория', related_name='subcategories')

    def get_absolute_url(self):
        pass

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"Категория: pk={self.pk}, title={self.title}"

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    """Модель Товара"""
    title = models.CharField(max_length=255, verbose_name='Наименование товара')
    price = models.FloatField(verbose_name='Цена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    watched = models.IntegerField(default=0, verbose_name='Просмотры')
    quantity = models.IntegerField(default=0, verbose_name='Количество на складе')
    description = models.TextField(default='Скоро здесь будет описание', verbose_name='Описание товара')
    info = models.TextField(default='Дополнительная информация о продукте', verbose_name='Информация о товаре')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория', related_name='products')
    slug = models.SlugField(unique=True, null=True)
    size = models.IntegerField(default=30, verbose_name='Размер в мм.')
    color = models.CharField(max_length=30, default='Серебро', verbose_name='Цвет/Материал')

    def get_absolute_url(self):
        pass

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"Товар: pk={self.pk}, title={self.title}, price={self.price}"

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Gallery(models.Model):
    """Модель для организации картинок у продукта"""
    image = models.ImageField(upload_to=unique_gallery_image_path, verbose_name='Изображение')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Галерея товаров'
