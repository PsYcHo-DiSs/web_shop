from django.contrib import admin
from .models import (Category, Product, Gallery, Review, Mail,
                     Customer, Order, OrderProduct, ShippingAddress)
from django.utils.safestring import mark_safe


class GalleryInline(admin.TabularInline):
    fk_name = 'product'
    model = Gallery
    extra = 1
    fields = ('image',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent', 'get_products_count')
    prepopulated_fields = {'slug': ('title',)}

    def get_products_count(self, obj):
        if obj.products:
            return str(len(obj.products.all()))
        return '0'

    get_products_count.short_description = 'Количество товара'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'category', 'quantity', 'price', 'created_at', 'size', 'color', 'get_product_image')
    list_editable = ('price', 'quantity', 'size', 'color')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('title', 'price')
    list_display_links = ('pk', 'title')
    inlines = (GalleryInline,)
    readonly_fields = ('watched',)

    def get_product_image(self, obj):
        if obj.images.all():
            return mark_safe(f'<img src="{obj.images.all()[0].image.url}" width="50" height="60">')
        return "-"

    get_product_image.short_description = 'Изображение товара'


admin.site.register(Gallery)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Отображение отзывов в админке"""
    list_display = ('pk', 'author', 'created_at')
    readonly_fields = ('author', 'text', 'created_at')


@admin.register(Mail)
class ReviewMail(admin.ModelAdmin):
    """Почтовые подписки"""
    list_display = ('pk', 'mail', 'user')
    readonly_fields = ('mail', 'user')


@admin.register(Order)
class ReviewOrder(admin.ModelAdmin):
    """Корзинка"""
    list_display = ('customer', 'order_date', 'is_completed', 'shipping')
    readonly_fields = ('customer', 'is_completed', 'shipping')
    list_filter = ('customer', 'is_completed')


@admin.register(Customer)
class ReviewCustomer(admin.ModelAdmin):
    """Заказчики"""
    list_display = ('user', 'first_name', 'last_name', 'email')
    readonly_fields = ('user', 'first_name', 'last_name', 'email', 'phone')
    list_filter = ('user',)


@admin.register(OrderProduct)
class ReviewOrderProduct(admin.ModelAdmin):
    """Товары в заказах"""
    list_display = ('product', 'order', 'product_quantity', 'added_at')
    readonly_fields = ('product', 'order', 'product_quantity', 'added_at')
    list_filter = ('product',)


@admin.register(ShippingAddress)
class ReviewShippingAddress(admin.ModelAdmin):
    """Адреса доставки"""
    list_display = ('customer', 'city', 'state')
    readonly_fields = ('customer', 'order', 'city', 'state', 'street')
    list_filter = ('customer',)
