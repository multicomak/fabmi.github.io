import sys, os, errno
import requests
import re
from bs4 import BeautifulSoup
from os.path import basename
import unicodecsv
import urlparse
import urllib
from external_data_extractor import *
from shared import *
import argparse
from gspreaddatafetcher import *
from categoryrender import *
from productrender import *

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

requests_session = requests.Session()
parser = argparse.ArgumentParser()
parser.add_argument('-i', action='store', dest='input_file_url',
                    help='Input File Url', required=True)
parser.add_argument('-c', action='store', dest='category',
                    help='Category', required=True)
parser.add_argument('-sc', action='store', dest='sub_category',
                    help='Sub Category', required=True)
parser.add_argument('-d', action='store', dest='destination_dir',
                    help='Destination Directory Name', required=True)
parser.add_argument('-s', action='store', dest='staging_dir',
                    help='Staging Dir')
parser.add_argument('--test', dest='isTest', action='store_true', default=False)
arguments = parser.parse_args()
rootDir = ""
if arguments.isTest is True:
	print "RUNNING in Test mode"
	rootDir = os.path.abspath(arguments.destination_dir)
spreadsheet_url = arguments.input_file_url

(category, productInfos) = fetchCategoryAndProductInfo(spreadsheet_url, arguments.sub_category)
outputdir = os.path.join(os.path.abspath(arguments.destination_dir), arguments.category, arguments.sub_category)
mkdir_p(outputdir)

for productInfo in productInfos:
	print "Fetching info for" + productInfo['productUrl']
	r = requests_session.get(productInfo['productUrl'])
	soup = BeautifulSoup(r.content)
	# if "flipkart" in site_url:
	# 	p  = extract_data_from_flipkart(soup)
	# elif "jabong" in site_url:
	# 	p  = extract_data_from_jabong(soup, productInfo)
	# elif "myntra" in site_url:
	# 	p  = extract_data_from_myntra(soup)
	# elif "amazon" in site_url:
	# 	p  = extract_data_from_amazon(soup)
	# elif "aliexpress" in site_url:
	# 	p  = extract_data_from_aliexpress(soup, tuple)
	try:
		if "jabong" in productInfo['productUrl']:
			p  = extract_data_from_jabong(soup)
		elif "flipkart" in productInfo['productUrl']:
		 	p  = extract_data_from_flipkart(soup)
		elif "myntra" in productInfo['productUrl']:
			p  = extract_data_from_myntra(soup)
		elif "amazon" in productInfo['productUrl']:
			p  = extract_data_from_amazon(soup)
	 	else:
	 		p = {}
		product = dict(productInfo.items() + p.items())
		if 'outOfStock'  in product:
			print "Out ot Stock" + product['productUrl']
			continue
		productImgForCategoryPage = []
		if 'productImgUrl' in product and product['productImgUrl'].strip() != '':
			images = product['productImgUrl'].strip().split('\n')
			productImgForCategoryPage = [{'std_img':img, 'zoom_img':img} for img in images]
			product['imageUrls'] = productImgForCategoryPage
		else:
			productImgForCategoryPage = product['imageUrls'][:2]
		product['productImg1Url'] = productImgForCategoryPage[0]['std_img']
		product['productImg2Url'] = productImgForCategoryPage[0]['std_img']
		if len(productImgForCategoryPage) > 1:
			product['productImg2Url'] = productImgForCategoryPage[1]['std_img']
		product = dict((k,v) for k, v in product.iteritems() if str(v).strip() != "")
		category.add_Product(product)
	except:
		print "Error Processing Product" + str(product)
		print "Unexpected error:", sys.exc_info()[0] 
		raise
renderCategory(category.__dict__, rootDir, os.path.join(os.path.abspath(arguments.destination_dir), arguments.category, arguments.sub_category + ".html"))
for product in category.products:
	categoryDictionary = category.__dict__
	dictionary = dict(product.items() + {"category": category.category, "subCategory": category.subCategory,"title":category.title}.items())
	renderProduct(dictionary, rootDir, os.path.join(outputdir, product['productCode'] + ".html"))