import gspread
import collections
import json
from productrender import *
from categoryrender import *


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
	gc = gspread.login('connect.fabmi@gmail.com', 'advikdarsh')
	sheet = gc.open_by_url(url)
	overview = sheet.worksheet("overview")
	productSheet = sheet.worksheet(productSheetName)
	overview_data_lists = overview.get_all_values()
	productSheet_data_lists = productSheet.get_all_values()
	data = {t[0]:t[1] for t in productSheet_data_lists[:8]}
	data['categoryDesc'] = [line.strip() for line in data['categoryDesc'].split('\n')]
	#c = Category(data("title"), data("categoryName"), data("categoryImgUrl"), data("categoryDesc"))
	c = Category(data['title'], data['category'], data['subCategory'], data['categoryImgUrl'], data['categoryDesc'])
	header = productSheet_data_lists[8]
	products = [productRow(header,x) for x in productSheet_data_lists[9:]]
	products = filter(isCurrent, products)
	for product in products:
		try:
			product['description'] = [line.strip() for line in product['description'].strip().split('\n')]
			if product['sizes'] is not "":
				product['sizes'] = [getDictionary(x.rstrip()) for x in product['sizes'].rstrip().split("\n")]
				product['sizeheaders'] = product['sizes'][0].keys()
			if product['colors'] is not "":
				colorsData = product['colors'].split("\n")
				product['colors'] = [getDictionary(x.rstrip()) for x in product['colors'].split("\n")]
		except:
			print "Error during processing:" + str(product);
			raise
	products.sort(key= lambda item : item['new'], reverse=True)
	return (c, products)

#fetchCategoryAndInfo("https://docs.google.com/spreadsheets/d/1bCEy3-vnDQVw8alQqb7hH9USr5SM7LRFfvGmJH-bxLc/edit#gid=13071765", "tops_shirts")