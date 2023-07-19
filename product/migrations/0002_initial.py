# Generated by Django 4.2.2 on 2023-07-12 14:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("product", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="userreviewsession",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="shoppingsession",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="promotion",
            name="products",
            field=models.ManyToManyField(
                related_name="product_list", to="product.product"
            ),
        ),
        migrations.AddField(
            model_name="productreview",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="product_reviews",
                to="product.product",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="category_products",
                to="product.productcategory",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="discount",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="discount_products",
                to="product.productdiscount",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="inventory",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="inventory_product",
                to="product.productinventory",
            ),
        ),
        migrations.AddField(
            model_name="orderitem",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="order_item_orders",
                to="product.order",
            ),
        ),
        migrations.AddField(
            model_name="orderitem",
            name="product",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="product_order",
                to="product.product",
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="payment",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="payment_order",
                to="product.payment",
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="cartitem",
            name="product",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="product_cart",
                to="product.product",
            ),
        ),
        migrations.AddField(
            model_name="cartitem",
            name="session",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="session_cart_items",
                to="product.shoppingsession",
            ),
        ),
    ]
