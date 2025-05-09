# Generated by Django 5.2 on 2025-05-06 22:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percentage', models.DecimalField(decimal_places=2, help_text='e.g., 10 for 10% discount', max_digits=5)),
                ('active', models.BooleanField(default=True)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='discounts', to='products.product')),
            ],
            options={
                'verbose_name': 'Discount',
                'verbose_name_plural': 'Discounts',
                'ordering': ['-start_date'],
            },
        ),
    ]
