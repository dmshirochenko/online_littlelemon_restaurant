# Generated by Django 4.2.5 on 2023-09-17 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("LittleLemonAPI", "0004_remove_order_delivery_crew"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="is_delivered",
            field=models.BooleanField(db_index=True, default=False),
        ),
    ]
