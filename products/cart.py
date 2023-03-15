# encapsulate cart functionality

from products.models import CartItem

class Cart(list):
	# boostrap cart in session
	pass

# use my bootstraped Cart class
def cart(request):
	request.session['cart'] = request.session.get('cart', [])
	_cart = request.session.get('cart', []).copy()
	# request.session['cart'] = _cart
	_already_seen_products = {
		# dictionary mapping of product id and associate cartitems in session
		# 1: CartItem(id=x, quantity=50),
		# 2: CartItem(id=7, quantity)
	}
	cart = Cart()
	add_to_cart = cart.append
	for i, id in enumerate(_cart):
		try:
			cart_item = CartItem.objects.get(id=id)
		except CartItem.DoesNotExist:
			# remove items in session that don't exists
			request.session['cart'].pop(i)
		else:
			# remove redundancy of items that point to the same product
			# if two items in the same session cart point to the same product
			# then they should be only one item 
			product_id = cart_item.product.id
			if product_id in _already_seen_products:
				# already seen increase the quantity instead of adding it to cart
				cart_item = _already_seen_products[product_id] # seen cart item
				cart_item.quantity += 1
			else:
				# cart.append(cart_item)
				_already_seen_products[cart_item.product.id] = cart_item
				add_to_cart(cart_item)
	return cart