from django.urls import path
from .views import(
    LoginView,
    RegisterView,
    CreateStaffView,
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('create-staff/', CreateStaffView.as_view(), name='create-staff'),
    
]
