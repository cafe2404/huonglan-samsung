# Generated by Django 5.1.7 on 2025-03-15 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_rename_formated_price_save_productmodel_formatted_price_save'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productmodel',
            name='ratings',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True),
        ),
    ]
