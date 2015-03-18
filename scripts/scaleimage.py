import argparse
import os
import subprocess

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
	                    help='Image Name', required=True)
	arguments = parser.parse_args()

	outputfile1 = outputdir = os.path.join(os.path.abspath(arguments.destination_dir), 'crop_' + arguments.image_name)
	outputfile2 = outputdir = os.path.join(os.path.abspath(arguments.destination_dir), 'pad_' + arguments.image_name)
	scaleimage(arguments.input_file_url, outputfile1, False)
	scaleimage(arguments.input_file_url, outputfile2, True)	
	# scaleimage('http://g02.a.alicdn.com/kf/HTB1aCBYHXXXXXa1XXXXq6xXFXXXF/220853895/HTB1aCBYHXXXXXa1XXXXq6xXFXXXF.jpg?size=283752&height=800&width=800&hash=80f505c9c4575b17159e0ba542657e9b', '/tmp/cut.jpg', arguments.isPad)

