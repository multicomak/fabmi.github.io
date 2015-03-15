from templateengine import renderTemplate
import codecs

class BreadCrumb(object):
	breadCrumbName = ""
	breadCrumbUrl = ""
	def __init__(self, breadCrumbName, breadCrumbUrl):
		self.breadCrumbName = breadCrumbName
		self.breadCrumbUrl = breadCrumbUrl

class ImageInfo(object):
	thumbnailUrl = ""
	standardUrl = ""
	def __init__(self, thumbnailUrl, standardUrl):
		self.thumbnailUrl = thumbnailUrl
		self.standardUrl = standardUrl

class Product(object):
	def __init__(self, title, price, productName, productCode, 
		productImg1Url, productImg2Url, mrp = None, new = False, discount = None, brand=None, outOfStock=False, productUrl=None):
		self.title = title
		self.price = price
		self.productName = productName
		self.productCode = productCode
		self.productImg1Url = productImg1Url
		self.productImg2Url = productImg2Url
		self.mrp = mrp
		self.new = new
		self.discount = discount
		self.brand = brand
		self.outOfStock = outOfStock
		self.productUrl = productUrl
		self.breadCrumbs = []
		self.imageInfos = []
		self.description = []

	def add_breadCrumb(self, breadCrumbName, breadCrumbUrl):
		self.breadCrumbs.append( BreadCrumb(breadCrumbName, breadCrumbUrl))

	def add_imageInfo(self, thumbnailUrl, standardUrl):
		self.imageInfos.append( ImageInfo(thumbnailUrl, standardUrl))

	def add_descriptionLine(self, line):
		self.description.append(line)


def renderProduct(dictionary, rootDir, outputfile):
	output = renderTemplate("product.html", dict(dictionary.items() + {"relativedir": rootDir}.items()))
	with codecs.open(outputfile, 'wb', "utf-8") as output_file:
		output_file.write(output)

# product = {"title":"FABMI- ABC", "breadcrumbs":["ABC", "Product"], "isexternalparty": True, "externalurl":"http://www.jabong.com/faballey-Blue-Solid-Top-1007955.html", "mrp":1500, "price":1000, "productname":"Awesome Jacket", "productcode":"ABC12345", "imageinfo":[{"standard":"images/products/big-jacket1.jpg","thumbnail":"images/products/big-jacket1.jpg"},{"standard":"images/products/big-jacket2.jpg","thumbnail":"images/products/big-jacket2.jpg"}]}
# d = Product("Hello", 200, "ABC", "XYZ", 300, None, False, "http://www.jabong.com/faballey-Blue-Solid-Top-1007955.html")
# d.add_breadCrumb("asdb","asdf")
# d.add_imageInfo("images/products/big-jacket1.jpg","images/products/big-jacket1.jpg")
# d.add_imageInfo("images/products/big-jacket2.jpg","images/products/big-jacket2.jpg")
# d.add_descriptionLine("Sed volutpat ac massa eget lacinia. Suspendisse non purus semper, tellus vel, tristique urna.")
# d.add_descriptionLine("Cumque nihil facere itaque mollitia consectetur saepe cupiditate debitis fugiat temporibus soluta maxime doloremque alias enim officia aperiam at similique quae vel sapiente nulla molestiae tenetur deleniti architecto ratione accusantium.")
# print d.__dict__
# renderProduct(d.__dict__, "../product_output.html")