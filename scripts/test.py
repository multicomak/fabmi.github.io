import sys, os, errno
import requests
import re
import traceback
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
from generateimages import *
from termcolor import colored


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
parser.add_argument('-idx', action='store', dest='only_index',
                    help='Process only these indices')
parser.add_argument('--test', dest='isTest', action='store_true', default=False)
arguments = parser.parse_args()
failedProducts = []
rootDir = ""
if arguments.isTest is True:
	print "RUNNING in Test mode"
	rootDir = os.path.abspath(arguments.destination_dir)
spreadsheet_url = arguments.input_file_url

(category, productInfos) = fetchCategoryAndProductInfo(spreadsheet_url, arguments.sub_category)
outputdir = os.path.join(os.path.abspath(arguments.destination_dir), arguments.category, arguments.sub_category)
mkdir_p(outputdir)
if arguments.only_index:
	print "Processing only indices " + arguments.only_index
	productInfos = [productInfos[int(index)] for index in arguments.only_index.split(",")]
for productInfo in productInfos:
	print "Fetching info for:" + productInfo['productUrl']
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
		elif "snapdeal" in productInfo['productUrl']:
			p  = extract_data_from_snapdeal(soup)
	 	else:
	 		p = {}
		if 'fabmiOwned' in productInfo and productInfo['fabmiOwned'] is not '':
			if productInfo['productImgUrl'] is "" and  productInfo['productImgOriginUrl'] is not "":
				setImageUrlsForFabmiOwnedProducts(productInfo, os.path.join(os.sep, 'images', category.category.lower(), category.subCategory, productInfo['productCode']), len(productInfo['productImgOriginUrl']))
		product = dict(productInfo.items() + p.items())
		if 'outOfStock'  in product:
			print colored("Out ot Stock" + product['productUrl'], "yellow")
			continue
		productImgForCategoryPage = []
		if 'productImgUrl' in product and len(product['productImgUrl']) > 0:
			images = product['productImgUrl']
			productImgForCategoryPage = [{'std_img':img, 'zoom_img':img} for img in images]
			product['imageUrls'] = productImgForCategoryPage
		elif 'imageUrls' in product:
			productImgForCategoryPage = product['imageUrls'][:2]
		if len(productImgForCategoryPage) > 0:
			product['productImg1Url'] = productImgForCategoryPage[0]['std_img']
			product['productImg2Url'] = productImgForCategoryPage[0]['std_img']
		if len(productImgForCategoryPage) > 1:
			product['productImg2Url'] = productImgForCategoryPage[1]['std_img']
		product = dict((k,v) for k, v in product.iteritems() if str(v).strip() != "")
		category.add_Product(product)
	except Exception, err:
		print "Error Processing Product" + str(productInfo)
		print(traceback.print_exc())
		failedProducts.append(productInfo['productUrl'])

renderCategory(category.__dict__, rootDir, os.path.join(os.path.abspath(arguments.destination_dir), arguments.category, arguments.sub_category + ".html"))
for product in category.products:
	categoryDictionary = category.__dict__
	dictionary = dict(product.items() + {"category": category.category, "categoryName": category.categoryName, "subCategory": category.subCategory,"title":category.title}.items())
	try:
		generateimages(dictionary, arguments.destination_dir)
		renderProduct(dictionary, rootDir, os.path.join(outputdir, product['productCode'] + ".html"))
	except:
		print "Error Processing Product:" + str(product)
		print "Unexpected error:", sys.exc_info()
		failedProducts.append(product['productUrl'])
if len(failedProducts) > 0:
	print "Error processing following products :" + str(failedProducts)