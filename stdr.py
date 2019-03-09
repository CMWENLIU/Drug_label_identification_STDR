# import all tools and libraries
import os
import re
#import cv2
import glob
#import spacy
import time
import datetime
import data_helpers
import process_image
#from fuzzywuzzy import fuzz
#from fuzzywuzzy import process
#import PIL
#from PIL import Image
from random import randint
#import matplotlib
#import matplotlib.pyplot as plt
#import pillowfight
#import numpy as np
import time
import pandas as pd
import sys
import pyocr
import pyocr.builders
import cropimage

print('All tools are imported successfully')

# Next is to prepare Tesseract OCR tools
tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)
# The tools are returned in the recommended order of usage
tool = tools[0]
print("Will use tool '%s'" % (tool.get_name()))
# Ex: Will use tool 'libtesseract'

langs = tool.get_available_languages()
print('Following languages are available:')
print(', '.join(langs))
language = 'eng'
# build globle variables:
all_res = [] 
dic = {'file': '-'}
for l in langs:
    dic[l] = '-'

all_files = [] #create list for all images

# Load all type of available image files
ext = ['jpg', 'png','bmp', 'jpeg','JPG', 'PNG', 'BMP', 'JPEG']

for root, dirs, files in os.walk("data/images/"):
    for file in files:
        if file.endswith(tuple(ext)):
             all_files.append(os.path.join(root, file))
print ('There are ' + str(len(all_files)) + ' images loaded')

#next to crop images:
start = time.time()
with open ('stdr.txt', 'w', encoding = 'utf-8') as writef:
  for f in all_files:
    cropimage.detection(f)
    s = data_helpers.clean_str(data_helpers.recog_crop(f, language, dic, tool))
    writef.write(s + '\n')
    print('file:  ' + f[-15:] + ' finished!' + 'Running time: ' + str(time.time()-start))



'''
#next to save cropped images:
with open ('stdr.txt', 'w', encoding = 'utf-8') as writef:
  for f in all_files:
    s = data_helpers.recog_crop(f, langs, dic, tool)
    writef.write(s + '\n')

for root, dirs, files in os.walk("data/results/"):
    for f in files:
        if f.endswith(tuple(ext)):
             all_files.append(os.path.join(root, f))
print ('There are ' + str(len(all_files)) + ' images loaded totally')

#Following we recognize all images and write to database.
print('Following we recognize all images and write all text to dataset.')
i = 1
with open('ocr.txt', 'w', encoding='utf-8') as outf:
  for f in sorted(all_files):
    try:
      result = data_helpers.ext_txt(f, langs, dic, tool)
    except:
      print('Error for: ' + f)
    time_str = datetime.datetime.now().isoformat()
    if i % 10 == 0 or i > (len(all_files)//10)*10:
        print("{}: {}/{} processed".format(time_str, i, len(all_files),))
    #all_res.append(result.copy())
    line = str(result['file']) + ' ' + str(result['eng'])
    outf.write(line + '\n')
    i += 1


df = pd.DataFrame(all_res)
#df.to_csv('result.csv', header=True, columns=['file', 'eng', 'fra', 'spa', 'chi_sim'], index=False)
df.to_csv('ocr.csv', encoding='utf_8_sig', header=True, columns=['file', 'eng'], index=False)
print('All images have been recognized and saved to result.csv')


with open('result.html', 'w') as outf:
    with open('htmlhead.txt', 'r') as fh:
        for line in fh:
            outf.write(line)
    imghead = '<img src="'
    #imgtail = '" onclick="changesize(this)">'
    imgtail = '">'
    for item in all_res:
        outf.write(imghead + item['file'] + imgtail)
        outf.write('<p>--file:' + os.path.basename(item['file']) + '</p>')
        outf.write('<p>--English:' + item['eng'] + '</p>')
        #outf.write('<p>--French:' + item['fra']+ '</p>')
        #outf.write('<p>--Spanish:' + item['spa'] + '</p>')
        #outf.write('<p>--Chinese:' + item['chi_sim'] + '</p>')
        outf.write('<hr>' + '\n')
    with open('htmltail.txt', 'r') as ft:
        for line in ft:
            outf.write(line)
print('All images have been recognized and saved to result.html')


from PIL import Image
 
def crop(image_path, coords, saved_location):
    """
    @param image_path: The path to the image to edit
    @param coords: A tuple of x/y coordinates (x1, y1, x2, y2)
    @param saved_location: Path to save the cropped image
    """
    image_obj = Image.open(image_path)
    cropped_image = image_obj.crop(coords)
    cropped_image.save(saved_location)
    cropped_image.show()


if __name__ == '__main__':
    image = '0.jpg'
    s = '25,167,89,178'
    w = s.split(',')
    print (len(w))
    b = int(s.replace(',',''))
    #crop(image, b, 'cropped.jpg')
'''
