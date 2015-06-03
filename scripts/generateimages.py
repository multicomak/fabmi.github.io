import argparse
import os
import subprocess
from os import listdir
from os.path import isfile, join
from urllib import pathname2url 
from urlparse import urlsplit, urlunsplit, parse_qsl
from urllib import urlencode
import urlnorm

def canonizeurl(url):
    split = urlsplit(urlnorm.norm(url))
    path = split[2].split(' ')[0]

    while path.startswith('/..'):
        path = path[3:]

    while path.endswith('%20'):
        path = path[:-3]

    qs = urlencode(sorted(parse_qsl(split.query)))
    return urlunsplit((split.scheme, split.netloc, path, qs, ''))

def scaleimage(imageurl, outputfile, pad):
	scaleType = ''
	if pad:
		scaleType = 'pad'
	else:
		scaleType = 'crop'
	subprocess.call(['./aspect', '300x420', '-m', scaleType, canonizeurl(imageurl), outputfile])

def scaleimagetofile(imageurl, outputdir, filename):
	outputfile1 = os.path.join(outputdir, filename)
	outputfile2 = os.path.join(outputdir, 'pad_' + filename)
	scaleimage(imageurl, outputfile1, False)
	scaleimage(imageurl, outputfile2, True)	

def setImageUrlsForFabmiOwnedProducts(product, directory, size):
	product['productImgUrl'] = [os.path.join(directory,'prod_' + str(i+1) + ".jpg") for i in range(0,size)]

def generateimages(product, rootdir):
	if 'fabmiOwned' in product:
		directory = os.path.join(os.path.abspath(rootdir), 'images', product['category'].lower(), product['subCategory'], product['productCode'])
		if os.path.exists(directory) is False:
			os.makedirs(directory)
		onlyfiles = [  os.path.basename(f) for f in listdir(directory) if isfile(join(directory,f))]
		if 'productImgUrl' not in product and  'productImgOriginUrl' in product:
			setImageUrlsForFabmiOwnedProducts(product, os.path.join(os.sep, 'images', product['category'].lower(), product['subCategory'], product['productCode']), len(product['productImgOriginUrl']))
		productimages = [os.path.basename(f) for f in product['productImgUrl']]
		if set(onlyfiles).issuperset(productimages):
			print "Product Images already exists hence not generating images: " + str(product['productCode'])
			return
		if 'productImgOriginUrl' in product:
			producturls = product['productImgOriginUrl']
			for idx, producturl in enumerate(producturls):
				scaleimagetofile(producturl, directory, 'prod_' + str(idx+1) + '.jpg')

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', action='store', dest='input_file_url',
	                    help='Input File Url', required=True)
	parser.add_argument('-d', action='store', dest='destination_dir',
	                    help='Destination Directory Name', required=True)
	# parser.add_argument('--pad', dest='isPad', action='store_true', default=False)
	parser.add_argument('-img', action='store', dest='image_name',
	                    help='Image Name', required=True)
	arguments = parser.parse_args()
	if os.path.exists(arguments.destination_dir) is False:
		os.makedirs(arguments.destination_dir)

	scaleimagetofile(arguments.input_file_url, arguments.destination_dir, arguments.image_name)
	# outputfile1 = os.path.join(os.path.abspath(arguments.destination_dir), 'crop_' + arguments.image_name)
	# outputfile2 = os.path.join(os.path.abspath(arguments.destination_dir), 'pad_' + arguments.image_name)
	# scaleimage(arguments.input_file_url, outputfile1, False)
	# scaleimage(arguments.input_file_url, outputfile2, True)
	subprocess.call(['nautilus',arguments.destination_dir])	
	# scaleimage('http://g02.a.alicdn.com/kf/HTB1aCBYHXXXXXa1XXXXq6xXFXXXF/220853895/HTB1aCBYHXXXXXa1XXXXq6xXFXXXF.jpg?size=283752&height=800&width=800&hash=80f505c9c4575b17159e0ba542657e9b', '/tmp/cut.jpg', arguments.isPad)

