from django.urls import path
from .views import (
    CategoryListView, 
    ProductListView, 
    ProductCreateView, 
    CreateCategoryView,
    CategoryUpdateView,
    ProductUpdateView
)

urlpatterns = [
    path('list-categories/', CategoryListView.as_view()),
    path('list-categories/<int:pk>/', CategoryListView.as_view()),
    path('list-products/', ProductListView.as_view()),
    path('list-products/<int:pk>/', ProductListView.as_view()),
    path('create-product/', ProductCreateView.as_view()),
    path('create-category/', CreateCategoryView.as_view()),
    path('update-category/<int:pk>/', CategoryUpdateView.as_view()),
    path('update-product/<int:pk>/', ProductUpdateView.as_view()),
]