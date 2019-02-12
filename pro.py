import os
import time
import collections
import pandas as pd
import numpy as np
from collections import Counter
from google_images_download import google_images_download   #importing the library
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

class Drug(object):
    """__init__() functions as the class constructor"""
    def __init__(self, name=None, text=None, label=None):
        self.name = name
        self.text = text
        self.label = label  


def download_images(label, key_words):
  response = google_images_download.googleimagesdownload()   #class instantiation
  argument = {"keywords": key_words, "limit":5, "image_directory": "images", "prefix": label} 
  paths = response.download(argument)

#split line in dm2000, then get finename, textContents and labels
def split_fname_texts(line):
  obj = {}
  if '.jpg' in line:
    obj['name'] = line.split('.jpg', 1)[0] + '.jpg'
    obj['text'] = line.split('.jpg', 1)[1]
    obj['label'] = line.split('_', 1)[0]
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
   
def frequency(druglist, n):
  label_list = []
  for item in druglist:
    label_list.append(item.label)
  counter=collections.Counter(label_list)
  result = []
  count_list = []
  fre = counter.values()
  fre_dis = collections.Counter(fre)
  df = pd.DataFrame({'distribution': fre_dis})
  df.to_csv('result.csv')
'''
  for item in counter:
    if counter[item] > n:
      result.append(item)
      count_list.append(counter[item])
  df = pd.DataFrame({'count':count_list})
  df.to_csv('result.csv')
  return result
'''
def cal_acu_5(df):
  a = np.zeros(shape=(df.shape[0], 4))
  row_list = []
  for index, row in df.iterrows():
    re_list = []
    #print "index is: " + str(index)
    obj = row['text']
    for i, r in df.iterrows():
      re_list.append(fuzz.partial_ratio(obj, r['text']))
    print sorted(re_list)[-5:-1]#top of the list
    #print sorted(re_list)[0:4]#bottom of the list
    row_list.append(sorted(re_list)[0:5])
  a = row_list
  return a
    
drug_list=[]#list of drugs to store fileName,Text and lablel information
with open('data/dm2000.txt', 'r') as rf:
  for line in rf:
    split_r = split_fname_texts(line)
    drug_list.append(Drug(split_r['name'], split_r['text'], split_r['label']))
print len(drug_list)
df = pd.DataFrame([vars(f) for f in drug_list])
df.columns = ["label", "name", "text"]
frequency(drug_list, 3)
#final_list = frequency(drug_list, 3)#get the records with count more than 3
#print len(final_list)
#print df['label']
#df = df[df['label'].isin(final_list)]
#print len(df)
#r_matrix = cal_acu_5(df)
#print r_matrix




