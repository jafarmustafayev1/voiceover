from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:actor_id>/', views.create_order, name='create_order'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('update/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('payment/<int:order_id>/', views.payment_view, name='payment'),
    path('payment-success/<int:order_id>/', views.payment_success, name='payment_success'),
]