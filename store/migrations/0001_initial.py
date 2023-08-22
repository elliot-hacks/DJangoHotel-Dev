# Generated by Django 4.2.4 on 2023-08-22 13:00

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import store.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asset', models.CharField(choices=[('C', 'COUNTER'), ('K', 'KITCHEN'), ('R', 'ROOMS')], default='C', max_length=1)),
            ],
            options={
                'ordering': ['asset'],
            },
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='store.asset')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('images', models.ImageField(default='uploads/product.png', upload_to='uploads/', validators=[store.validators.validate_file_size])),
                ('slug', models.SlugField()),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(1)])),
                ('stock', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('bought_at', models.DateTimeField(auto_now_add=True)),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='store.collection')),
            ],
            options={
                'ordering': ['name', 'collection', 'stock', 'price'],
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment', models.CharField(choices=[('CASH', 'CASH'), ('M-PESA', 'M-PESA'), ('HALO-PESA', 'HALO-PESA'), ('AIRTEL-MONEY', 'AIRTEL-MONEY'), ('TIGO-PESA', 'TIGO-PESA'), ('NMB', 'NMB-BANK'), ('CRDB', 'CRDB-BANK'), ('KCB', 'KCB-BANK'), ('PAYPAL', 'PAYPAL')], default='CASH', max_length=15)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
            options={
                'ordering': ['product'],
            },
        ),
    ]
