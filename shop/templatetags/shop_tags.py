from django import template
from shop.models import Category, Product, FavouriteProducts
from django.template.defaulttags import register as range_register
from django.core.cache import cache
from django.db.models import Count, Q

from shop.cart import get_cart_data

register = template.Library()


@register.simple_tag()
def get_subcategories(category):
    """Получение списка подкатегорий"""
    return Category.objects.filter(parent=category)


@register.simple_tag()
def get_sorted():
    sorters = [
        {
            'title': 'Цена',
            'sorters': [
                ('price', 'по возрастанию'),
                ('-price', 'по убыванию')
            ]
        },

        {
            'title': 'Цвет',
            'sorters': [
                ('color', 'от А до Я'),
                ('-color', 'от Я до А')
            ]
        },

        {
            'title': 'Размер',
            'sorters': [
                ('size', 'по возрастанию'),
                ('-size', 'по убыванию')
            ]
        }
    ]

    return sorters


@range_register.filter
def get_positive_range(value):
    return range(value)


@range_register.filter
def get_negative_range(value):
    return range(5 - value)


@register.simple_tag()
def get_favourite_products(user):
    """вывод избранных товаров на страничку"""
    fav = FavouriteProducts.objects.filter(user=user)
    products = [i.product for i in fav]
    return products


@register.simple_tag()
def get_fav_prods_qty(user):
    """получение количества товаров в списке избранного"""
    return len(get_favourite_products(user))


@register.simple_tag()
def get_cart_total_quantity(request):
    """получение количества единиц товаров в корзине"""
    cart_total_quantity = get_cart_data(request)['cart_total_quantity']
    return cart_total_quantity
