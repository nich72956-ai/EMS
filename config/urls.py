from django.contrib import admin
from django.urls import path, include
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),

    path('products/', include('products.urls')),
    path('customers/', include('customers.urls')),
    path('invoices/', include('invoices.urls')),
    path('suppliers/', include('suppliers.urls')),
    path('purchases/', include('purchases.urls')),
    path('reports/', include('reports.urls')),
]