# Generated by Django 4.2.2 on 2023-07-31 18:21

from django.db import migrations, models
import django.db.models.deletion
import product.models.ad
import product.models.cart_item
import product.models.category
import product.models.discount
import product.models.inventory
import product.models.order_item
import product.models.product
import product.models.shopping_session


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CartItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("quantity", models.IntegerField(default=1)),
            ],
            options={
                "verbose_name": "Cart Item",
                "verbose_name_plural": "Cart Items",
            },
            managers=[
                ("objects", product.models.cart_item.CartItemManager()),
            ],
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "total",
                    models.DecimalField(decimal_places=2, default=0, max_digits=16),
                ),
            ],
            options={
                "verbose_name": "Order",
                "verbose_name_plural": "Orders",
            },
            managers=[
                ("objects", product.models.order_item.OrderManager()),
            ],
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("quantity", models.IntegerField(default=1)),
            ],
            options={
                "verbose_name": "Order Item",
                "verbose_name_plural": "Order Items",
            },
        ),
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("amount", models.IntegerField(default=0)),
                ("provider", models.CharField(max_length=100)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Packaging", "Packaging"),
                            ("processing", "Processing"),
                            ("dispatching", "Dispatching"),
                            ("shipping", "Shipping"),
                            ("delivery", "Delivery"),
                        ],
                        default="processing",
                        max_length=30,
                    ),
                ),
            ],
            options={
                "verbose_name": "Payment",
                "verbose_name_plural": "Payments",
            },
            managers=[
                ("objects", product.models.order_item.PaymentManager()),
            ],
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("name", models.CharField(max_length=200)),
                ("desc", models.TextField()),
                ("sku", models.CharField(blank=True, max_length=25, null=True)),
                ("brand_name", models.CharField(max_length=150)),
                (
                    "price",
                    models.DecimalField(decimal_places=2, default=0, max_digits=16),
                ),
                (
                    "delivery_type",
                    models.CharField(
                        choices=[
                            ("standard_delivery", "Standard delivery"),
                            ("express_delivery", "Express delivery"),
                            ("international_delivery", "International delivery"),
                            ("in_store_pick_up", "In-Store Pickup"),
                        ],
                        default="in_store_pick_up",
                        max_length=30,
                    ),
                ),
                (
                    "shipping_type",
                    models.CharField(
                        choices=[
                            ("postal_service", "Postal Service"),
                            ("courier_services", "Couriers Services"),
                        ],
                        default="postal_service",
                        max_length=30,
                    ),
                ),
            ],
            options={
                "verbose_name": "Product",
                "verbose_name_plural": "Products",
            },
            managers=[
                ("objects", product.models.product.ProductManager()),
            ],
        ),
        migrations.CreateModel(
            name="ProductAd",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        upload_to=product.models.ad.product_ad_directory_path
                    ),
                ),
                ("name", models.CharField(max_length=150)),
                ("slug", models.SlugField(max_length=255, unique=True)),
            ],
            options={
                "verbose_name": "Product Ad",
                "verbose_name_plural": "Product Ads",
            },
        ),
        migrations.CreateModel(
            name="ProductCategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("name", models.CharField(max_length=100)),
                ("desc", models.TextField()),
                (
                    "banner",
                    models.ImageField(
                        upload_to=product.models.category.product_category_directory_path
                    ),
                ),
            ],
            options={
                "verbose_name": "Product Category",
                "verbose_name_plural": "Product Categories",
            },
            managers=[
                ("objects", product.models.category.ProductCategoryManager()),
            ],
        ),
        migrations.CreateModel(
            name="ProductDiscount",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "code",
                    models.CharField(blank=True, max_length=20, null=True, unique=True),
                ),
                ("desc", models.TextField()),
                (
                    "discount_percent",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                ("active", models.BooleanField(default=False)),
            ],
            options={
                "verbose_name": "Product Discount",
                "verbose_name_plural": "Product Discounts",
            },
            managers=[
                ("objects", product.models.discount.ProductDiscountManager()),
            ],
        ),
        migrations.CreateModel(
            name="ProductInventory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("quantity", models.IntegerField(default=0)),
            ],
            options={
                "verbose_name": "Product Inventory",
                "verbose_name_plural": "Product Inventories",
            },
            managers=[
                ("objects", product.models.inventory.ProductInventoryManager()),
            ],
        ),
        migrations.CreateModel(
            name="ProductReview",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("rating", models.IntegerField()),
                ("desc", models.TextField()),
            ],
            options={
                "verbose_name": "Product Review",
                "verbose_name_plural": "Product Reviews",
            },
        ),
        migrations.CreateModel(
            name="Promotion",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "prom_type",
                    models.CharField(
                        choices=[
                            ("discount", "Discount"),
                            ("coupon_code", "Coupon Code"),
                            ("free_shipping", "Free Shipping"),
                            ("flash_sale", "Flash Sale"),
                        ],
                        default="discount",
                        max_length=30,
                    ),
                ),
                ("state_date", models.DateTimeField()),
                ("end_date", models.DateTimeField()),
            ],
            options={
                "verbose_name": "Promotion",
                "verbose_name_plural": "Promotions",
            },
        ),
        migrations.CreateModel(
            name="ShoppingSession",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "subtotal",
                    models.DecimalField(decimal_places=2, default=0, max_digits=16),
                ),
            ],
            options={
                "verbose_name": "Shopping Session",
                "verbose_name_plural": "Shopping Sessions",
            },
            managers=[
                ("objects", product.models.shopping_session.ShoppingSessionManager()),
            ],
        ),
        migrations.CreateModel(
            name="UserReviewSession",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "review",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_review_sessions",
                        to="product.productreview",
                    ),
                ),
            ],
            options={
                "verbose_name": "User Review Session",
                "verbose_name_plural": "User Review Sessions",
            },
        ),
    ]
