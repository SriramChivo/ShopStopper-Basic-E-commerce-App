from django.contrib import admin
from .models import Tags, Products, Orders, Customer, State

# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    model = Orders
    readonly_fields = ["UpdatedTime", "dateCreated"]


admin.site.register(Tags)
admin.site.register(Products)
admin.site.register(Orders, OrderAdmin)
admin.site.register(Customer)
admin.site.register(State)
