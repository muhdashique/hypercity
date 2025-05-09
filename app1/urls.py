from django.urls import path # type: ignore
from django.conf import settings # type: ignore
from django.conf.urls.static import static # type: ignore
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-data/', views.add_data, name='add_data'),
    path('logout/', views.logout, name='logout'),
    path('add_customer/', views.add_customer, name='add_customer'),
    path('edit_customer/<int:customer_id>/', views.edit_customer, name='edit_customer'),
    path('delete_customer/<int:customer_id>/', views.delete_customer, name='delete_customer'),
    path('export-customers/', views.export_customers_excel, name='export_customers'),
]
   
    
