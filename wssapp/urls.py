from django.urls import path
from . import views

urlpatterns = [
    path('stock/', views.stock_view, name='stock_view'),
]
