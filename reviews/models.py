from django.db import models
from users.models import Customer
from products.models import Product
# Create your models here.
class Review(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='user_reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} - {self.product} - {self.rating}'

    class Meta:
        unique_together = ('user', 'product')
        ordering = ['-created_at']


class Comment(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='user_comments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_comments')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} - {self.product} - {self.comment}'

    class Meta:
        ordering = ['-created_at']

class Reply(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='user_replies')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_replies')
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} - {self.comment} - {self.reply}'

    class Meta:
        ordering = ['-created_at']


    