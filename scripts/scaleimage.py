import argparse
import os
from os import system
import subprocess
import string

def addoverlay(productname, price, inputfile, outputfile):
	command_template = string.Template("convert -background '#00000080' -pointsize 25 -fill '#FF7579' label:' FabMi    $productname    Rs $price ' miff:- | composite -gravity south -geometry +0+10 - $inputfile   $outputfile")
	values = {'productname':productname, 'price':price, 'inputfile':inputfile, 'outputfile':outputfile}
	command = command_template.substitute(values)
	print command
	os.system(command)
	# subprocess.call([command)

def scaleimage(imageurl, outputfile, pad):
	scaleType = ''
	if pad:
		scaleType = 'pad'
	else:
		scaleType = 'crop'
	subprocess.call(['./aspect', '300x420', '-m', scaleType, imageurl, outputfile])

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', action='store', dest='input_file_url',
	                    help='Input File Url', required=True)
	parser.add_argument('-d', action='store', dest='destination_dir',
	                    help='Destination Directory Name', required=True)
	# parser.add_argument('--pad', dest='isPad', action='store_true', default=False)
	parser.add_argument('-img', action='store', dest='image_name',
	                    help='Image Name')
	parser.add_argument('-n', action='store', dest='productname',
	                    help='Product Name', required=True)
	parser.add_argument('-p', action='store', dest='price',
	                    help='Product Price', required=True)
	arguments = parser.parse_args()
	if arguments.image_name is None:
		arguments.image_name = arguments.productname.replace(" ", "").lower() + ".jpg"
	outputfile1 = outputdir = os.path.join(os.path.abspath(arguments.destination_dir), arguments.image_name)
	# outputfile2 = outputdir = os.path.join(os.path.abspath(arguments.destination_dir), 'pad_' + arguments.image_name)
	scaleimage(arguments.input_file_url, outputfile1, False)
	addoverlay(arguments.productname, arguments.price, outputfile1, outputfile1)
	# scaleimage(arguments.input_file_url, outputfile2, True)	
	# scaleimage('http://g02.a.alicdn.com/kf/HTB1aCBYHXXXXXa1XXXXq6xXFXXXF/220853895/HTB1aCBYHXXXXXa1XXXXq6xXFXXXF.jpg?size=283752&height=800&width=800&hash=80f505c9c4575b17159e0ba542657e9b', '/tmp/cut.jpg', arguments.isPad)

