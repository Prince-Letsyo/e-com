from django.contrib import admin
from product.admin import (OrderInline, UserReviewSessionInline, ShoppingSessionInline)

from user.models.user import User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    inlines = [
        ShoppingSessionInline, 
        OrderInline,
        UserReviewSessionInline
        ]
    list_display = ['username', 'email', ]
    search_fields = ['username']


admin.site.register(User, UserAdmin)