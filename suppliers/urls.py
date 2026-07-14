from django.urls import path
from . import views

urlpatterns = [
    path('', views.supplier_list, name='supplier_list'),
     path('add/', views.add_supplier, name='add_supplier'),
]