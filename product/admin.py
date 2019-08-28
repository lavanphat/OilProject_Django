from django.contrib import admin
# Register your models here.
from django.contrib.auth.models import Group

from product.models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    list_per_page = 10
    search_fields = ('title',)


class BrandAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    list_per_page = 10
    search_fields = ('title',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'Price_Import', 'Price_New', 'Wage', 'Quality', 'Active')
    list_per_page = 10
    search_fields = ('title', 'slug')
    list_filter = ('Active', 'Brand', 'Date_Create', 'Date_Update')
    list_editable = ('Active', 'Price_Import', 'Price_New', 'Wage', 'Quality',)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'Price','Active')
    list_per_page = 10
    search_fields = ('title',)
    list_filter = ('Active',)
    list_editable = ('Active',)


admin.site.unregister(Group)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Service, ServiceAdmin)
