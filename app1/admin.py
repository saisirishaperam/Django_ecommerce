from django.contrib import admin
from .models import Product,Coustomer_Details,Cart,Payment,OrderPlaced,Wishlist,Order_Placed,Contact

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'brand', 'selling_price', 'discount_price','category', 'product_image')
    search_fields = ('title', 'brand', 'category')
    list_filter = ('category', 'brand')



@admin.register(Coustomer_Details)
class CustomerDetailsAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'mobile', 'category', 'city', 'pincode', 'state', 'country')
    search_fields = ('name', 'mobile', 'city', 'state')
    list_filter = ('category', 'state', 'country')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'total_cost')
    search_fields = ('user__username', 'Product__title')
    list_filter = ('user',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'razorpay_order_id', 'razorpay_payment_id', 'paid']
    search_fields = ['user__username', 'razorpay_order_id', 'razorpay_payment_id']
    list_filter = ['paid']

@admin.register(OrderPlaced)
class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer', 'product', 'quantity', 'ordered_date', 'status', 'payment']
    list_filter = ['status', 'ordered_date']
    search_fields = ['user__username', 'product__title', 'customer__name']

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product']
    search_fields = ['user__username', 'product__title']


@admin.register(Order_Placed)
class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'product',
        'quantity',
        'total_cost',
        'status',
        'ordered_date',
        'delivered_on',
    )
    list_filter = ('status', 'ordered_date')
    search_fields = ('user__username', 'product__title', 'full_address')
    readonly_fields = ('ordered_date', 'delivered_on', 'total_cost')

    def delivered_on(self, obj):
        return obj.delivered_on

    def total_cost(self, obj):
        return obj.total_cost
    
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

