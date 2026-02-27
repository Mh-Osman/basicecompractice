from rest_framework import serializers
from .models import Review, Comment, Reply
from users.models import Customer
from products.models import Product

from rest_framework.request import Request

class CustomerMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'email']

class ReplySerializer(serializers.ModelSerializer):
    user_details = CustomerMinimalSerializer(source='user', read_only=True)

    class Meta:
        model = Reply
        fields = ['id', 'user', 'user_details', 'comment', 'reply', 'created_at', 'updated_at']
        read_only_fields = ['user']

class CommentSerializer(serializers.ModelSerializer):
    user_details = CustomerMinimalSerializer(source='user', read_only=True)
    replies = ReplySerializer(source='comment_replies', many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'user_details', 'product', 'comment', 'replies', 'created_at', 'updated_at']
        read_only_fields = ['user']

class ReviewSerializer(serializers.ModelSerializer):
    user_details = CustomerMinimalSerializer(source='user', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'user_details', 'product', 'rating', 'review', 'created_at', 'updated_at']
        read_only_fields = ['user']

    def validate(self, attrs):
        request = self.context.get('request')
        if not request or not request.user:
            return attrs
        
        user = request.user
        product = attrs.get('product')

        # If it's a creation request, ensure product is provided and unique for the user
        if not self.instance:
            if not product:
                raise serializers.ValidationError({"product": "This field is required."})
            if Review.objects.filter(user=user, product=product).exists():
                raise serializers.ValidationError("You have already reviewed this product.")
        
        # If it's an update, we usually don't want to change the product, 
        # but if we do, we should check uniqueness excluding the current instance
        elif product:
            if Review.objects.filter(user=user, product=product).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("You have already reviewed this product.")

        return attrs
