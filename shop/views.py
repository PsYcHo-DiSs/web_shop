from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.core.cache import cache

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

        top_products = cache.get('top_products')
        if top_products is None:
            top_products = Product.objects.order_by('-watched')[:8]
            cache.set('top_products', top_products, timeout=60)  # кеш на 60 секунд

        context['top_products'] = top_products
        return context


class CategoryProductsView(ListView):
    """Вывод подкатегорий на отдельной странице"""
    model = Product
    context_object_name = 'products'
    extra_context = {'title': 'Дочерние категории'}
    template_name = 'shop/category_page.html'

    def dispatch(self, request, *args, **kwargs):
        self.parent_category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """Получить все товары подкатегории"""
        subcategories = self.parent_category.subcategories.all()

        type_field = self.request.GET.get('type')
        if type_field:
            products = Product.objects.filter(category__slug=type_field)
        else:
            products = Product.objects.filter(category__in=subcategories).order_by('?')

        return products

    def get_context_data(self, *, object_list=None, **kwargs):
        """Дополнительные элементы в виде категории"""
        context = super().get_context_data()
        parent_category = self.parent_category
        context['category'] = parent_category
        context['title'] = parent_category.title
        return context
