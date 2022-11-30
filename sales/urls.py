from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    path('', views.map, name='map'),
    path('<int:product_id>/', views.detail, name='detail'),
    path('product/create/', views.product_create, name='product_create'),
    path('product/modify/<int:product_id>/', views.product_modify, name='product_modify'),
    path('product/delete/<int:product_id>/', views.product_delete, name='product_delete'),
    path('product/product_list/', views.index, name='index'),
    path('salesinfo/', views.salesinfo_index, name='salesinfo_index'),
    path('salesinfo/<int:salesinfo_id>/', views.salesinfo_detail, name='salesinfo_detail'),
    path('salesinfo/crete/', views.salesinfo_create, name='salesinfo_create'),
    path('salesinfo/modify/<int:salesinfo_id>/', views.salesinfo_modify, name='salesinfo_modify'),
    path('salesinfo/delete/<int:salesinfo_id>/', views.salesinfo_delete, name='salesinfo_delete'),
]