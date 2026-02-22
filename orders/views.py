from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from .models import Order, OrderItem, Cart, CartItem
from products.models import Product
from .serializers import OrderSerializer, CartSerializer, CartItemSerializer

class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def post(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()

        return Response({'message': 'Product added to cart'}, status=status.HTTP_201_CREATED)

    def patch(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')

        if not product_id or quantity is None:
            return Response({'error': 'Product ID and quantity are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
            cart_item.quantity = int(quantity)
            cart_item.save()
            return Response({'message': 'Cart updated'})
        except CartItem.DoesNotExist:
            return Response({'error': 'Item not found in cart'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        cart = Cart.objects.get(user=request.user)
        product_id = request.data.get('product_id')
        
        if product_id:
            CartItem.objects.filter(cart=cart, product_id=product_id).delete()
            return Response({'message': 'Item removed from cart'})
        else:
            CartItem.objects.filter(cart=cart).delete()
            return Response({'message': 'Cart cleared'})

class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)
        items = cart.items.all()
        shipping_address = request.data.get('shipping_address')

        if not items:
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not shipping_address:
            return Response({'error': 'Shipping address is required'}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(
            user=user,
            shipping_address=shipping_address,
            total_price=0
        )

        total_price = 0
        for cart_item in items:
            product = cart_item.product
            quantity = cart_item.quantity

            if product.stock < quantity:
                transaction.set_rollback(True)
                return Response({'error': f'Not enough stock for {product.name}'}, status=status.HTTP_400_BAD_REQUEST)

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )

            product.stock -= quantity
            product.save()

            total_price += product.price * quantity

        order.total_price = total_price
        order.save()

        # Clear the cart
        items.delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class OrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.is_superuser or user.role == 'staff':
            orders = Order.objects.all()
        else:
            orders = Order.objects.filter(user=user)
        
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
