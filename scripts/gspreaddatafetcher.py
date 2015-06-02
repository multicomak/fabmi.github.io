import sys, os, errno
import gspread
import collections
import json
from productrender import *
from categoryrender import *
from oauth2client.client import SignedJwtAssertionCredentials

def productRow(header, row):
	return dict(zip(header, row))

def isCurrent(x):
	return x['current'].lower() == "true"

def compare(item1, item2):
	return (item1['new'] < item2['new'])

def getDictionary(data):
	data = unicode(data, "utf-8")
	decoder = json.JSONDecoder(object_pairs_hook=collections.OrderedDict)
	return decoder.decode(data)

def fetchCategoryAndProductInfo(url, productSheetName):
	json_key = json.load(open('FABMI-42acf5218e38.json'))
	scope = ['https://spreadsheets.google.com/feeds']	
	# gc = gspread.login('connect.fabmi@gmail.com', 'advikdarsh')
	credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
	gc = gspread.authorize(credentials)
	sheet = gc.open_by_url(url)
	overview = sheet.worksheet("overview")
	productSheet = sheet.worksheet(productSheetName)
	overview_data_lists = overview.get_all_values()
	productSheet_data_lists = productSheet.get_all_values()
	overview_data_lists = overview.get_all_values()
	overview_data = {t[0]:t[1] for t in overview_data_lists}

	data = {t[0]:t[1] for t in productSheet_data_lists[:8]}
	# data['categoryDesc'] = [line.strip() for line in data['categoryDesc'].split('\n')]
	data['dos'] = [line.strip() for line in data['dos'].strip().split('\n')]
	data['donts'] = [line.strip() for line in data['donts'].strip().split('\n')]	
	#c = Category(data("title"), data("categoryName"), data("categoryImgUrl"), data("categoryDesc"))
	c = Category(data['title'], data['category'], overview_data['categoryName'], data['subCategory'], data['categoryImgUrl'], data['dos'], data['donts'])
	header = productSheet_data_lists[8]
	products = [productRow(header,x) for x in productSheet_data_lists[9:]]
	products = filter(isCurrent, products)
	for product in products:
		try:
			if product['description'].strip() is not '':
				product['description'] = [line.strip() for line in product['description'].strip().split('\n')]
			if product['productImgUrl'].strip() is not '':
				product['productImgUrl'] = [line.strip() for line in product['productImgUrl'].strip().split('\n')]
			if product['productImgOriginUrl'].strip() is not '':			
				product['productImgOriginUrl'] = [line.strip() for line in product['productImgOriginUrl'].strip().split('\n')]
			if product['sizes'].strip() is not "":
				product['sizes'] = [getDictionary(x.strip()) for x in product['sizes'].strip().split("\n")]
				product['sizeheaders'] = product['sizes'][0].keys()
			if product['colors'].strip() is not "":
				# colorsData = product['colors'].rstrip().split("\n")
				product['colors'] = [getDictionary(x.strip()) for x in product['colors'].strip().split("\n")]
		except:
			print "product:" + str(product)
			print "Unexpected error:", sys.exc_info()
			raise
	products.sort(key= lambda item : item['new'], reverse=True)
	return (c, products)

#fetchCategoryAndInfo("https://docs.google.com/spreadsheets/d/1bCEy3-vnDQVw8alQqb7hH9USr5SM7LRFfvGmJH-bxLc/edit#gid=13071765", "tops_shirts")