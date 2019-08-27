from django.contrib import admin

from .models import *


# Register your models here.
class BillProductInline(admin.StackedInline):
    extra = 0
    model = Bill_Product


class BillServiceInline(admin.StackedInline):
    extra = 0
    model = Bill_Service


class BillAdmin(admin.ModelAdmin):
    list_display = ('id', 'Date_Create', 'Total_Money', 'Sale', 'Active')
    list_per_page = 10
    search_fields = ('id', 'Total_Money')
    list_filter = ('Active', 'Date_Create',)
    list_editable = ('Active', )
    inlines = [BillProductInline,BillServiceInline]


admin.site.register(Bill, BillAdmin)
