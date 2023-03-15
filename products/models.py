import builtins
import math
from django.db import models
from django.utils import timezone

MAX_DECIMAL_PLACE = 2


def round(digit):
    # round it but clear .00 not neccessary in the case of 5.00
    rounded = builtins.round(digit, MAX_DECIMAL_PLACE)
    if rounded - math.floor(rounded) == 0:
        return math.floor(rounded)
    else:
        return rounded


# if a product is deleted associated images and cartitems will be deleted
# images no biggy but people might need to be informed of the cart
# depending on the design of the project
class Product(models.Model):
    price = models.DecimalField("old price", max_digits=9, decimal_places=MAX_DECIMAL_PLACE)
    discount = models.DecimalField(max_digits=3, decimal_places=MAX_DECIMAL_PLACE, help_text="The discount ratio.",)
    size = models.PositiveIntegerField("shoe size", default=35, help_text="The shoe size.")
    quantity = models.PositiveBigIntegerField(default=1)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    def getimage(self):
        images = self.images.all()
        if images:
            return images[0]
    
    def discount_rate(self):
        # the return value cannot be used in accounting since it's the approximate
        rate = self.discount
        return round((self.price)/((1-rate) or 1))
    
    def __str__(self):
        return 'NewShoe:{0}${1}'.format(self.id, self.price)


class ProductImage(models.Model):
    image = models.ImageField(upload_to="productimages", height_field=None, width_field=None, max_length=None)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    
    def __str__(self):
        return "1 of (%s) images" % (self.product.images.count())


