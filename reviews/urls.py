from django.urls import path
from .views import (
    ReviewListCreateView, ReviewDetailView,
    CommentListCreateView, CommentDetailView,
    ReplyCreateView, ReplyDetailView
)

urlpatterns = [
    path('reviews/', ReviewListCreateView.as_view(), name='review-list'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
    path('comments/', CommentListCreateView.as_view(), name='comment-list'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    
    path('comments/<int:comment_pk>/reply/', ReplyCreateView.as_view(), name='reply-create'),
    path('replies/<int:pk>/', ReplyDetailView.as_view(), name='reply-detail'),
]
