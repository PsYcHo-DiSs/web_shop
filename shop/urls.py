from django.urls import path
from .views import *

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('category/<slug:slug>/', CategoryProductsView.as_view(), name='category_detail'),
]
