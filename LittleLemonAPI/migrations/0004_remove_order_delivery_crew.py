# Generated by Django 4.2.5 on 2023-09-17 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("LittleLemonAPI", "0003_alter_order_assigned_to_alter_order_delivery_crew"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="delivery_crew",
        ),
    ]
