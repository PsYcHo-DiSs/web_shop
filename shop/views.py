from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Category, Product


class Index(ListView):
    """Класс представления главной тсраницы"""
    model = Product
    extra_context = {'title': 'Главная страница'}
    template_name = 'shop/index.html'
