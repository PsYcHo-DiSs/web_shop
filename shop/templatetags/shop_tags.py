from django import template
from shop.models import Category, Product
from django.core.cache import cache
from django.db.models import Count, Q

register = template.Library()


@register.simple_tag()
def get_subcategories(category):
    """Получение списка подкатегорий"""
    return Category.objects.filter(parent=category)
