import argparse
import os
import subprocess
from os import listdir
from os.path import isfile, join

def scaleimage(imageurl, outputfile, pad):
	scaleType = ''
	if pad:
		scaleType = 'pad'
	else:
		scaleType = 'crop'
	subprocess.call(['./aspect', '300x420', '-m', scaleType, imageurl, outputfile])

def scaleimagetofile(imageurl, outputdir, filename):
	outputfile1 = os.path.join(outputdir, 'crop_' + filename)
	outputfile2 = os.path.join(outputdir, 'pad_' + filename)
	scaleimage(imageurl, outputfile1, False)
	scaleimage(imageurl, outputfile2, True)	

def generateimages(product, rootdir):
	if 'fabmiOwned' in product:
		directory = os.path.join(os.path.abspath(rootdir), 'images', product['category'].lower(), product['subCategory'], product['productCode'])
		print directory
		if os.path.exists(directory) is False:
			os.makedirs(directory)
		onlyfiles = [  os.path.basename(f) for f in listdir(directory) if isfile(join(directory,f))]
		productimages = [os.path.basename(f) for f in product['productImgUrl']]
		if set(onlyfiles).issuperset(productimages):
			print "Product Images already exists hence not generating images: " + str(product['productCode'])
			return
		if 'productImgOriginUrl' in product:
			producturls = product['productImgOriginUrl'].rstrip().split('\n')
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

	outputfile1 = os.path.join(os.path.abspath(arguments.destination_dir), 'crop_' + arguments.image_name)
	outputfile2 = os.path.join(os.path.abspath(arguments.destination_dir), 'pad_' + arguments.image_name)
	scaleimage(arguments.input_file_url, outputfile1, False)
	scaleimage(arguments.input_file_url, outputfile2, True)
	subprocess.call(['nautilus',arguments.destination_dir])	
	# scaleimage('http://g02.a.alicdn.com/kf/HTB1aCBYHXXXXXa1XXXXq6xXFXXXF/220853895/HTB1aCBYHXXXXXa1XXXXq6xXFXXXF.jpg?size=283752&height=800&width=800&hash=80f505c9c4575b17159e0ba542657e9b', '/tmp/cut.jpg', arguments.isPad)

