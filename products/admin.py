from django.contrib import admin

from . import models


class ProductImageInline(admin.StackedInline):
    model = models.ProductImage

class ProductModel(admin.ModelAdmin):
    exclude = ['date_created', 'date_modified']
    search_fields = ['price', 'discount', 'size', 'quantity']
    
    inlines = [ProductImageInline]
    

admin.site.register(models.Product, ProductModel)