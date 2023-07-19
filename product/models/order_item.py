from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from helper import TimeStampsWithOrder, StatusOrder
from product.models.product import Product
from user.models.utils import UserOnToOne


class PaymentManager(models.Manager):
    use_in_migrations = True

    def get_payment_order(self, payment):
        try:
            return payment.payment_order
        except ObjectDoesNotExist:
            return None


class Payment(TimeStampsWithOrder):
    amount = models.IntegerField(default=0)
    provider = models.CharField(max_length=100)
    status = models.CharField(
        choices=StatusOrder.choices, default=StatusOrder.PROCESSING, max_length=30
    )

    objects = PaymentManager()

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"

    def __str__(self):
        return f"Amount: {self.amount} payed through {self.provider}"


class OrderManager(models.Manager):
    use_in_migrations = True

    def get_order_item_order(self, order):
        return order.order_item_order.all()


class Order(UserOnToOne, TimeStampsWithOrder):
    total = models.DecimalField(decimal_places=2, default=0, max_digits=16)
    payment = models.OneToOneField(
        Payment, on_delete=models.CASCADE, related_name="payment_order"
    )

    objects = OrderManager()

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"{self.user.get_username()} made a total of {self.total} order"


class OrderItem(TimeStampsWithOrder):
    order = models.ForeignKey(
        Order, related_name="order_item_orders", on_delete=models.CASCADE
    )
    product = models.OneToOneField(
        Product, related_name="product_order", on_delete=models.CASCADE
    )
    quantity = models.IntegerField(default=1)

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"

    def __str__(self):
        return f"{self.order.user.get_username()} place {self.quantity} order(s) for {self.product.name}"
