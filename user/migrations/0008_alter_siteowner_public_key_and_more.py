# Generated by Django 4.2.2 on 2023-07-21 21:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0007_remove_siteowner_iv_siteowner_site"),
    ]

    operations = [
        migrations.AlterField(
            model_name="siteowner",
            name="public_key",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="siteowner",
            name="secret_key",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
