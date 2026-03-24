from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.core.cache import cache
from django.contrib.auth import login, logout
from django.contrib import messages

from .models import Category, Product, Review
from .forms import LoginForm, RegistrationForm, ReviewForm


class Index(ListView):
    """Класс представления главной страницы"""
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
        self.parent_category = get_object_or_404(Category, slug=self.kwargs['slug'])  # noqa
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """Получить все товары подкатегории"""
        subcategories = self.parent_category.subcategories.all()

        if type_field := self.request.GET.get('type'):
            products = Product.objects.filter(category__slug=type_field)
            return products

        products = Product.objects.filter(category__in=subcategories).order_by('?')

        if sort_field := self.request.GET.get('sort'):
            products = products.order_by(sort_field)

        return products

    def get_context_data(self, *, object_list=None, **kwargs):
        """Дополнительные элементы в виде категории"""
        context = super().get_context_data()
        parent_category = self.parent_category
        context['category'] = parent_category
        context['title'] = parent_category.title
        return context


class ProductDetailView(DetailView):
    """Вывод подробностей о товаре на отдельной странице"""

    model = Product
    context_object_name = 'product'
    template_name = 'shop/product_page.html'

    def get_context_data(self, **kwargs):
        """Вывод на страницу доп элементов"""
        context = super().get_context_data()
        product = self.object
        product.increment_views()

        similar_products = Product.objects.filter(category=product.category).exclude(slug=product.slug)

        context['title'] = product.title
        context['product'] = product
        context['similar_products'] = similar_products

        # получение отзывов, принадлежащих продукту (сортировка по primary key, в обратном порядке)
        reviews = Review.objects.filter(product=product).order_by('-pk')
        context['reviews'] = reviews
        context['avg_grade'] = 0

        if len(reviews) != 0:
            total_grade = sum([r.grade for r in reviews])
            avg_grade = int(total_grade / len(reviews))
            context['avg_grade'] = avg_grade

        if self.request.user.is_authenticated:
            context['review_form'] = ReviewForm()

        return context


def login_registration(request):
    context = {'title': 'Войти или зарегистрироваться',
               'login_form': LoginForm,
               'registration_form': RegistrationForm}

    return render(request, 'shop/login_registration.html', context)


def user_login(request):
    """Аутентификация пользователя"""
    form = LoginForm(data=request.POST)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('index')

    messages.error(request, message='Неверное имя пользователя или пароль')
    return redirect('login_registration')


def user_logout(request):
    """Выход пользователя"""
    logout(request)
    return redirect('index')


def user_registration(request):
    """Регистрация пользователя"""
    form = RegistrationForm(data=request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Аккаунт пользователя успешно создан")
    else:
        for error in form.errors:
            messages.error(request, form.errors[error].as_text())
        # messages.error(request, message='Что то пошло не так')
    return redirect('login_registration')


def save_review(request, product_pk):
    """Сохранить отзыв"""
    form = ReviewForm(data=request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.author = request.user
        product = Product.objects.get(pk=product_pk)
        review.product = product
        review.save()
        return redirect('product_detail', product.slug)
