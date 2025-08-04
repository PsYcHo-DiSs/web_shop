from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Category, Product


class Index(ListView):
    """Класс представления главной тсраницы"""
    model = Category
    context_object_name = 'categories'
    extra_context = {'title': 'Главная страница'}
    template_name = 'shop/index.html'

    def get_queryset(self):
        """Вывод родительской категории"""
        categories = Category.objects.filter(parent=None)
        return categories

    def get_context_data(self, *, object_list=None, **kwargs):
        """Вывод на страничку дополнительных элементов из 8 самых популярных товаров"""
        context = super().get_context_data()
        context['top_products'] = Product.objects.order_by('-watched')[:8]
        return context

class CategoryProductsView(ListView):
    """Вывод подкатегорий на отдельной странице"""
    model = Product
    context_object_name = 'products'
    extra_context = {'title': 'Дочерние категории'}
    template_name = 'shop/category_page.html'

    def get_queryset(self):
        """Получить все товары подкатегории"""
        parent_category = Category.objects.get(slug=self.kwargs['slug'])
        subcategories = parent_category.subcategories.all()
        products = Product.objects.filter(category__in=subcategories).order_by('?')
        return products
