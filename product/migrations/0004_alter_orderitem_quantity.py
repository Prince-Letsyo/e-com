# Generated by Django 4.2.2 on 2023-07-12 23:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0003_remove_shoppingsession_total_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orderitem",
            name="quantity",
            field=models.IntegerField(default=1),
        ),
    ]
