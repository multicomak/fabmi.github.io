from productrender import BreadCrumb
from templateengine import renderTemplate
import codecs

class ProductInfo(object):
	def __init__(self, productName, productUrl, productImg1Url, productImg2Url, price, mrp = None, new = False, discount = None):
		self.productName = productName
		self.productUrl = productUrl
		self.productImg1Url = productImg1Url
		self.productImg2Url = productImg2Url
		self.price = price
		self.mrp = mrp
		self.new = new
		self.discount = discount

class Category(object):
	def __init__(self, title, category, subCategory, categoryImgUrl, dos, donts):
		self.title = title
		self.category = category
		self.subCategory = subCategory
		self.categoryImgUrl = categoryImgUrl
		self.dos = dos
		self.donts = donts		
		self.breadCrumbs = []
		self.products = []
	
	def add_breadCrumb(self, breadCrumbName, breadCrumbUrl):
		self.breadCrumbs.append( BreadCrumb(breadCrumbName, breadCrumbUrl))
	
	def add_Product(self, product):
		self.products.append(product)

def renderCategory(dictionary, rootDir, outputfile):
	output = renderTemplate("category.html", dict(dictionary.items() + {"relativedir": rootDir}.items()))
	with codecs.open(outputfile, 'wb', "utf-8") as output_file:
		output_file.write(output)

# c = Category("Tops", "Tops", "images/products/category-show.png", "Aenean dictum libero vitae magna sagittis, eu convallis dolor blandit. Fusce consectetur tincidunt pretium. Etiam non tellus massa. Aenean tincidunt in augue nec tempus. Nulla porta libero sit amet lorem pellentesque posuere...")
# c.add_breadCrumb("Tops", "category_output.html")
# c.add_Product(ProductInfo("Top1", "product_output.html", "images/products/item1.jpg", "images/products/item1-hover.jpg", 200, 300, True, 33))
# c.add_Product(ProductInfo("Top2", "product_output.html", "images/products/item2.jpg", "images/products/item2-hover.jpg", 200, 300, True, 33))
# c.add_Product(ProductInfo("Top2", "product_output.html", "images/products/item2.jpg", "images/products/item2-hover.jpg", 200, 300, False, 33))
# c.add_Product(ProductInfo("Top2", "product_output.html", "images/products/item2.jpg", "images/products/item2-hover.jpg", 200, 300, False, 33))
# c.add_Product(ProductInfo("Top2", "product_output.html", "images/products/item2.jpg", "images/products/item2-hover.jpg", 200, 300, False, 33))
# c.add_Product(ProductInfo("Top2", "product_output.html", "images/products/item2.jpg", "images/products/item2-hover.jpg", 200, 300, False, 33))
# c.add_Product(ProductInfo("Top2", "product_output.html", "images/products/item2.jpg", "images/products/item2-hover.jpg", 200, 300, False, 33))
# c.add_Product(ProductInfo("Top2", "product_output.html", "images/products/item2.jpg", "images/products/item2-hover.jpg", 200, 300, False, 33))
# c.add_Product(ProductInfo("Top2", "product_output.html", "images/products/item2.jpg", "images/products/item2-hover.jpg", 200, 300, False, 33))
# renderCategory(c.__dict__, "../category_output.html")