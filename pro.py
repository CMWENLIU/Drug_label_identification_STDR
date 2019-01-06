import os
import time



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

  dic = Counter(name_list)
  print(len(dic))
  new_dic = dict((k, v) for k, v in dic.iteritems() if v > 3)
  print(len(new_dic))


with open('data/dm2000.txt', 'r') as myfile:
  for line in myfile:
    b = split_fname_texts(line)
    print b['label']
     
   
