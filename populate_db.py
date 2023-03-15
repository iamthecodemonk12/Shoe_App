import os, sys
import random, imghdr

from django.db.models.fields.files import ImageFieldFile, ImageField

from products.models import Product

def is_image(file):
	try:
		x = imghdr.what(file)
	except OSError:
		pass
	else:
		if x:
			return True
	return False


def create_entry(pic):
	product = Product()
	product.price = random.randint(0, 50)
	product.discount = random.randint(0, 100)
	product.size = random.randint(0, 25)
	product.image = ImageFieldFile(product, product.image, pic)
	return product


def create_entries():
	PICTURE_FOLDER = 'media/product_images'
	_pic = lambda p: os.path.join(PICTURE_FOLDER, p)
	pictures = os.listdir(PICTURE_FOLDER)
	for file in pictures:
		if is_image(_pic(file)):
			print('creating new product')
			product = create_entry(os.path.join('product_images', file))
			try:
				product.save()
			except Exception as e:
				print('An error occured while saving')
				print('\t\t', e, file=sys.stderr)