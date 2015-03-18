import sys, os, errno

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise
        
class Data:
	image_url = ""
	price = ""
	disc_price = ""
	out_of_stock = False
	product_code = ""
	embed_google_form = False
	def __init__(self, url, price, disc_price, out_of_stock=False, product_code="", embed_google_form=False):
		self.image_url = url
		self.price = price
		self.disc_price = disc_price
		self.out_of_stock = out_of_stock
		self.product_code = product_code
		self.embed_google_form = embed_google_form
