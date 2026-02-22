from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer

class CategoryListView(APIView):
    permission_classes = [AllowAny]             
    def get(self, request, pk=None):
        if pk:
            categories = Category.objects.filter(id=pk)
        else:
            categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CreateCategoryView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user= request.user
        data = request.data
        name = data.get('name')
        if user is None:
            return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
      
        if user.is_superuser or user.role == 'staff':
            if Category.objects.filter(name=name).exists():
                return Response({'error': 'Category already exists'}, status=status.HTTP_400_BAD_REQUEST)
            category = Category.objects.create(
                name=name,
            )
            return Response({'message': 'Category created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'User is not authorized'}, status=status.HTTP_403_FORBIDDEN)
class CategoryUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, pk):
        user= request.user
        data = request.data
        name = data.get('name')
        if user is None:
            return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
      
        if user.is_superuser or user.role == 'staff':
            try:
                category = Category.objects.get(id=pk)
                category.name = name
                category.save()
                return Response({'message': 'Category updated successfully'}, status=status.HTTP_200_OK)
            except Category.DoesNotExist:
                return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'User is not authorized'}, status=status.HTTP_403_FORBIDDEN)

class ProductListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, pk=None):
        if pk:
            products = Product.objects.filter(id=pk)
        else:
            products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProductCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user= request.user
        data = request.data
        name = data.get('name')
        description = data.get('description')
        price = data.get('price')
        image = data.get('image')
        stock = data.get('stock')
        stock_alarm = data.get('stock_alarm')
        category = data.get('category') # id of category
        category_obj = None
        if category:
            try:
                category_obj = Category.objects.get(id=category)
            except Category.DoesNotExist:
                return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if category_obj is None:
            return Response(
                {'error': 'Category not found'},
                status=status.HTTP_404_NOT_FOUND)
        
        if not name or not description or not price or not image or not stock  or not category:
            return Response(
                {'error': 'name, description, price, image, stock, category fields are required'},
                status=status.HTTP_400_BAD_REQUEST)
        if user is None:
            return Response(
                {'error': 'User is not authenticated'},
                status=status.HTTP_401_UNAUTHORIZED)
      
        if user.is_superuser or user.role == 'staff':
            product = Product.objects.create(
                name=name,
                description=description,
                price=price,
                image=image,
                stock=stock,
                stock_alarm=stock_alarm,
                category=category_obj
            )
            return Response({'message': 'Product created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'User is not authorized'}, status=status.HTTP_403_FORBIDDEN)
           


class ProductUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, pk):
        user= request.user
        data = request.data
        name = data.get('name')
        description = data.get('description')
        price = data.get('price')
        image = data.get('image')
        stock = data.get('stock')
        stock_alarm = data.get('stock_alarm')
        category_id = data.get('category')

        if user is None:
            return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        if not (user.is_superuser or user.role == 'staff'):
            return Response({'error': 'User is not authorized'}, status=status.HTTP_403_FORBIDDEN)

        try:
            product = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        if category_id:
            try:
                category_obj = Category.objects.get(id=category_id)
                product.category = category_obj
            except Category.DoesNotExist:
                return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

        if name: product.name = name
        if description: product.description = description
        if price: product.price = price
        if image: product.image = image
        if stock is not None: product.stock = stock
        if stock_alarm is not None: product.stock_alarm = stock_alarm

        product.save()
        return Response({'message': 'Product updated successfully'}, status=status.HTTP_200_OK)



