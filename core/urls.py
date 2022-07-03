from django.contrib import admin
from django.urls import path
from bank import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.process_payment, name='payment'),
    path('payment-history', views.payment_history, name='payment_history'),
]
