from django.urls import path
from .views import *

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('category/<slug:slug>/', CategoryProductsView.as_view(), name='category_detail'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('login_registration/', login_registration, name='login_registration')
]
