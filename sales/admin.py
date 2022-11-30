from django.contrib import admin
from django.contrib import admin
from .models import Product, SalesInfo


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    search_fields = ['pcode']

admin.site.register(Product, ProductAdmin)

class SalesAdmin(admin.ModelAdmin):
    search_fields = ['scode']

admin.site.register(SalesInfo, SalesAdmin)
