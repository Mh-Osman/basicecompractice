from django.urls import path
from .views import CheckoutView, OrderListView, CartView

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('my-orders/', OrderListView.as_view(), name='my-orders'),

]
