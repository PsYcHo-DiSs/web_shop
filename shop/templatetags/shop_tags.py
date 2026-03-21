from django import template
from shop.models import Category, Product
from django.template.defaulttags import  register as range_register
from django.core.cache import cache
from django.db.models import Count, Q

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