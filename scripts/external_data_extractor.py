import urlparse
from bs4 import BeautifulSoup
import sys, os
import requests
import re
from filehelper import *
from shared import *
from productrender import *

requests_session = requests.Session()

def extract_data_from_jabong(soup):
	image_url = []
	price = ""
	disc_price = ""
	mrp = ""
	out_of_stock = soup.find("div", class_="prd-sold-out")
	if out_of_stock is not None:
		return	{"outOfStock": True}
	for ul in soup.find_all("ul", class_ = "imageview-slider"):
		for li in ul.findAll('li'):
			std_img = ""
			if li.img.has_attr('src'):
				std_img = li.img.attrs['src'].strip()
			elif li.img.has_attr('data-src-onload'):
				std_img = li.img.attrs['data-src-onload'].strip()
			image_url.append({"std_img":std_img,"zoom_img":std_img})

	productCode = soup.find("td", {"id" : "qa-sku"}).string.strip()
	productName = soup.find("span", {"id" : "qa-title-product"}).string.strip()
	price = soup.find("span", {"itemprop" : "price"}).string.strip()
	disc_price_node = soup.find("div", {"id" : "pdp-voucher-price"})
	if disc_price_node is not None:
		mrp = price
		price = disc_price_node.string.replace("Rs.", "").strip()
	return {"imageUrls": image_url, "price": price, "mrp": mrp, "productCode":productCode, "productName":productName}

def extract_data_from_flipkart(soup):
	image_url = []
	price = ""
	images = soup.find_all("img", class_ = "productImage")
	out_of_stock = soup.find("div", {'class' : ["out-of-stock", "listing-obsolete-section"]})
	if out_of_stock is not None:
		return	{"outOfStock": True}
	for img in images:
		std_img = img.attrs['data-src'].strip()
		zoom_img = img.attrs['data-zoomimage'].strip()
		image_url.append({"std_img":std_img,"zoom_img":zoom_img})
	price = soup.find("meta", {"itemprop" : "price"}).attrs['content'].strip()
	productCode = soup.find("input", class_ = "btn-buy-now btn-big  current").attrs['data-pid']
	return {"imageUrls": image_url, "price": price, "productCode":productCode}

def extract_data_from_myntra(soup):
	image_url = []
	price = ""
	out_of_stock = soup.find("div", class_="oos")
	if out_of_stock is not None:
		return	{"outOfStock": True}
	thumbs = soup.find("div", class_ = "thumbs")
	for img in thumbs.find_all("img"):
		std_img = img.attrs['data-blowup'].strip()
		image_url.append({"std_img":std_img,"zoom_img":std_img})
	price = soup.find("div", class_ = "price").attrs['data-discountedprice'].strip()
	productCode = soup.find("h4", class_ = "id pdt-code").string.split(":")[1].strip()
	productName = soup.find("h1", class_="title").string.strip()
	return {"imageUrls": image_url, "price": price, "productCode":productCode, "productName":productName}

def extract_data_from_amazon(soup):
	image_url = []
	price = ""
	disc_price = ""
	productCode = ""
	out_of_stock = soup.find("div", {"id" : "availability_feature_div"})
	if out_of_stock is not None:
		children = out_of_stock.findChildren()
		if len(children) > 0 and "in stock" not in str(children).lower():
			return	{"outOfStock": True}
	for img in soup.find_all("img", class_= "a-dynamic-image"):
		std_img = img.attrs['src']
		image_url.append({"std_img":std_img,"zoom_img":std_img})
	price_div = soup.find("span", {"id" : "priceblock_ourprice"})
	if price_div is None:
		price_div = soup.find("span", {"id" : "priceblock_saleprice"})
	price =  price_div.text.replace(",","").replace(".00", "").replace(".50","").strip()	
	product_detail_feature_div =  soup.find("div", {"id":"detail_bullets_id"})
	ul = product_detail_feature_div.find("ul")
	li =  ul.find('li')
	productCode = li.text.replace("ASIN:", "").strip()
	return {"imageUrls": image_url, "price": price, "productCode":productCode}

# def extract_data_from_aliexpress(soup, tuple):
# 	url = tuple[0]
# 	image_url = ""
# 	price = tuple[2]
# 	disc_price = ""
# 	image_index = tuple[3]
# 	url_parsed = urlparse.urlparse(url)
# 	path_elems = url_parsed.path.split("/")
# 	product_id = path_elems[len(path_elems) -1].split(".")[0]
# 	product_desc_url = "http://desc.aliexpress.com/getDescModuleAjax.htm?productId=$1"
# 	r = requests_session.get(product_desc_url.replace("$1", product_id))
# 	product_soup = BeautifulSoup(r.content)
# 	images_on_page =  product_soup.findAll("img")
# 	current_product_img_counter = 0
# 	for img in images_on_page:
# 		if ".alicdn" in img.attrs['src']:
# 			if current_product_img_counter == int(image_index):
# 				image_url = img.attrs['src']
# 				break
# 			current_product_img_counter += 1
# 	#downloadfile(image_url, "/tmp", product_id)
# 	d = Data(image_url, price, disc_price, False, product_id, True)
# 	return d
