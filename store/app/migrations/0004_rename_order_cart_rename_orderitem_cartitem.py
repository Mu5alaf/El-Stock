# Generated by Django 4.2.13 on 2024-06-09 11:15

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0003_alter_order_total_amount'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Order',
            new_name='Cart',
        ),
        migrations.RenameModel(
            old_name='OrderItem',
            new_name='CartItem',
        ),
    ]
