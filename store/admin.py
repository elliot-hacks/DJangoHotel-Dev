from django.contrib import admin, messages
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet
from django.utils.html import format_html, urlencode
from django.urls import reverse
from django.contrib import messages
from . import models


# Register your models here.
class StockFilter(admin.SimpleListFilter):
    title = 'stock'
    parameter_name = 'stock'

    def lookups(self, request, model_admin):
        return [('<10', 'Low')]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    prepopulated_fields = {'slug': ['name'], 'description': ['name']}
    list_display = ['name', 'price', 'stock', 'bought_at', 'collection_title']
    list_editable = ['stock']
    list_filter = ['collection', 'bought_at', StockFilter]
    list_per_page = 10
    list_select_related = ['collection']
    actions = ['clear_inventory']
    search_fields = ['name']

    class Media:
        css = {
            'all': ['store/style.css']
        }

    def collection_title(self, product):
        return product.collection.name

    @admin.display(ordering='stock')
    def inventory_status(self, product):
        if product.stock < 10:
            return 'Low'
        return 'OK'

    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(stock=0)
        self.message_user(request, f'{updated_count} products were successfully updated.', messages.ERROR)


    #In addition for stock
    


@admin.register(models.Payment)
class PaymentAdmin(admin.ModelAdmin):
    autocomplete_fields = ['product']
    list_select_related = ['product']
    list_display = ['product', 'payment', 'price_sold', 'stock_available']
    search_fields = ['product', 'price', 'payment']
    list_editable = ['payment']

    @admin.display(ordering='price')
    def price_sold(self, price):
        url = (
            reverse('admin:store_product_changelist')
            + '?'
            + urlencode({
                'price__id': str(price.id)
            }))
        return format_html('<a href="{}">{} Products</a>', url, price.product.price)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(price_sold=Count('product'))

    @admin.display(ordering='stock')
    def stock_available(self, stock):
        url = (
            reverse('admin:store_product_changelist')
            + '?'
            + urlencode({
                'stock__id': str(stock.id)
            }))
        return format_html('<a href="{}">{} Products</a>', url, stock.product.stock)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(stock_available=Count('product'))

    def save_model(self, request, obj, form, change):
        if not obj.product:
            messages.error(request, "Cannot order null products.")
            return

        if obj.product.stock > 0:
            obj.product.stock -= 1
            obj.product.save()
        else:
            messages.error(request, "The product is out of stock.")
            return

        obj.save()

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    #autocomplete_fields = ['featured_product']
    list_display = ['name', 'products_count']
    search_fields = ['name']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (
            reverse('admin:store_product_changelist')
            + '?'
            + urlencode({
                'collection__id': str(collection.id)
            }))
        return format_html('<a href="{}">{} Products</a>', url, collection.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count=Count('products'))


@admin.register(models.Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ['asset', 'assets_available']
    search_fields = ['asset']

    @admin.display(ordering='assets_available')
    def assets_available(self, asset):
        url = (
            reverse('admin:store_product_changelist')
            + '?'
            + urlencode({
                'asset__id': str(asset.id)
            }))
        return format_html('<a href="{}">{} Collections</a>', url, asset.assets_available)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(assets_available=Count('collection'))
