from django.contrib import admin

from .models import Cart, CartItem, Order, OrderItem


# Define the inline model admin for OrderItem
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


# Register your models here.
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["user", "created_at"]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ["cart", "product", "quantity"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["user", "created_at", "total_price"]
    inlines = [OrderItemInline]
    readonly_fields = ["user", "created_at", "total_price"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["order", "product", "quantity", "price"]
    readonly_fields = ["order", "product", "quantity", "price"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
