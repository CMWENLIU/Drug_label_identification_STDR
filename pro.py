import os
import time
from google_images_download import google_images_download   #importing the library
  
def download_images(label, key_words):
  response = google_images_download.googleimagesdownload()   #class instantiation
  argument = {"keywords": key_words, "limit":5, "image_directory": "images", "prefix": label} 
  paths = response.download(argument)

def split_fname_texts(line):
  obj = {}
  if '.jpg' in line:
    obj['name'] = line.split('.jpg', 1)[0] + '.jpg'
    obj['text'] = line.split('.jpg', 1)[1]
    obj['label'] = obj['name'].rsplit('_', 1)[0]
  return obj

def construt(filepath):
  name_list, string_list = [], []
  with open(filepath, 'r') as rf:  
    for line in rf:
      if '.jpg' in line:
        splitted = line.split('.jpg', 1)
        name_list.append(splitted[0][:-1])
        string_list.append(splitted[1])

def split_keywords(line):
  obj = {}
  if '_' in line:
    split = line.split('_', 1)
    obj['label'] = split[0]
    obj['keywords'] = split[1] 
  return obj
   

#download_images('thyu66666__', 'herb drug')
lista=[]
with open('data/label_key.txt', 'r') as rf:
  for line in rf:
    lista.append(split_keywords(line)['label'])
print len(lista)
listb = set(lista)
print len(listb)
for i in range(len(lista)-1):
  if lista[i] == lista[i+1]:
    print lista[i]

