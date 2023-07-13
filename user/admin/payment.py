from django.contrib import admin
from user.models.payment import UserPayment


class UserPaymentAdmin(admin.ModelAdmin):

    list_display = ['user', 'provider', 'account_no', "expiry"]
    list_filter = ['user', 'provider',  "expiry"]
    search_fields = ['username']


admin.site.register(UserPayment, UserPaymentAdmin)

class UserPaymentInline(admin.StackedInline):
    extra=0
    model =  UserPayment

