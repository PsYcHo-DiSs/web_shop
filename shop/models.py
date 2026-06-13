from django.db import models
from django.db.models import F
from django.urls import reverse
from django.templatetags.static import static
from django.contrib.auth.models import User

from .utils import unique_category_image_path, unique_gallery_image_path


class Category(models.Model):
    """Модель категории товаров"""

    title = models.CharField(max_length=150, verbose_name='Наименование категории')
    image = models.ImageField(upload_to=unique_category_image_path, null=True, blank=True, verbose_name='Изображение')
    slug = models.SlugField(unique=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                               verbose_name='Категория', related_name='subcategories')

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"Категория: pk={self.pk}, title={self.title}"

    def get_absolute_url(self):
        """Ссылка на страницу родительской категории"""
        return reverse('category_detail', kwargs={'slug': self.slug})

    def get_parent_category_image_or_default(self):
        """Получение картинки родительской категории"""
        if self.image:
            return self.image.url

        return static('shop/img/net-kartinki.jpg')

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
        return reverse('product_detail', kwargs={'slug': self.slug})

    def increment_views(self):
        self.watched = F('watched') + 1
        self.save(update_fields=['watched'])
        self.refresh_from_db(fields=['watched'])

    def get_first_image_or_default(self):
        if self.images.exists():
            return self.images.first().image.url

        return static('shop/img/net-kartinki.jpg')

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


class Review(models.Model):
    """Модель для отзывов"""

    class Rating(models.IntegerChoices):
        TERRIBLE = 1, 'Ужасно'
        POOR = 2, 'Плохо'
        AVERAGE = 3, 'Нормально'
        GOOD = 4, 'Хорошо'
        EXCELLENT = 5, 'Отлично'

    text = models.TextField(verbose_name='Текст отзыва')
    grade = models.IntegerField(choices=Rating.choices, blank=True, null=True, verbose_name='Оценка')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата')

    def __str__(self):
        return self.author.username

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class FavouriteProducts(models.Model):
    """Модель для избранного"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'Избранный товар'
        verbose_name_plural = 'Избранные товары'


class Mail(models.Model):
    """Почтовая рассылка"""
    mail = models.EmailField(unique=True, verbose_name="Почта")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Пользователь")

    class Meta:
        verbose_name = "Почта"
        verbose_name_plural = "Почты"


class Customer(models.Model):
    """Контактная информация покупателя"""
    user = models.OneToOneField(User, models.SET_NULL, blank=True, null=True, verbose_name="Пользователь")
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='Почта')
    phone = models.CharField(max_length=255, verbose_name='Контактный номер')

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = "Покупатель"
        verbose_name_plural = "Покупатели"


class Order(models.Model):
    """Корзина покупателя"""
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True,
                                 verbose_name='Покупатель')
    order_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заказа')
    is_completed = models.BooleanField(default=False, verbose_name='Завершён')
    shipping = models.BooleanField(default=True, verbose_name='Доставка')

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    @property
    def get_cart_total_price(self):
        """для получения суммы товаров с корзины"""
        order_products = self.ordered.all()
        total_price = sum([p.get_order_product_total_price() for p in order_products])
        return total_price

    @property
    def get_order_total_qty(self):
        """для получения общего количества товаров из корзины заказа"""
        order_products = self.ordered.all()
        total_qty = sum([p.product_quantity for p in order_products])
        return total_qty


class OrderProduct(models.Model):
    """Заказ"""
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name="Наименование товара")
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, related_name='ordered')
    product_quantity = models.IntegerField(default=0, null=True, blank=True, verbose_name="Количество в заказе")
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Товар в заказе"
        verbose_name_plural = "Товары в заказах"

    @property
    def get_order_product_total_price(self):
        """считает total price заказа"""
        return self.product.price * self.product_quantity
