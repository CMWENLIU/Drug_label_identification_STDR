from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from uploads.core.models import Document
from uploads.core.forms import DocumentForm
import cropimage
import os
import data_helpers
import pyocr
import pro
import pandas as pd


def home(request):
    documents = Document.objects.all()
    return render(request, 'core/home.html', { 'documents': documents })

def top(request):
    class Drug(object):
        """__init__() functions as the class constructor"""
        def __init__(self, name=None, text=None, label=None):
            self.name = name
            self.text = text
            self.label = label  
    drug_list, test_string=[], ''#list of drugs to store fileName,Text and lablel information
    with open('data/ocr.txt', 'r') as rf:
      for line in rf:
        split_r = pro.split_fname_texts(line)
        drug_list.append(Drug(split_r['name'], split_r['text'], split_r['label']))
    df = pd.DataFrame([vars(f) for f in drug_list])
    df.columns = ["label", "name", "text"]
    #final_list = pro.frequency(drug_list, 4)#get the records with count more than n
    #df = df[df['label'].isin(final_list)]
    '''
    files = os.listdir('media')
    final_files = df['name'].tolist()
    for f in files:
      if any(f in s for s in final_files):
        pass
      else:
        os.remove(os.path.join('media/', f))
    '''
    with open('single_rec.txt', 'r') as readf:
        test_string = readf.readline()
    r, r1 = pro.cal_top(df, 10, test_string)
    res_names = r['result_name'].tolist()
    res_scores = r['result_score'].tolist()
    res_texts = r['result_text'].tolist()
    zipped = zip(res_names, res_scores, res_texts)
    with open('passpa.txt', 'r') as rpass:
        imagefile = rpass.readline().rstrip('\n')
        uploaded_file_url = rpass.readline().rstrip('\n')
        result_file_url = rpass.readline().rstrip('\n')
    return render(request, 'core/top.html', {'recognition': test_string, 'uploaded_file_url': uploaded_file_url, 'result_file_url': result_file_url, 'zipped': zipped})

def recognize(request):
    uploaded_file_url = ''
    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print("No OCR tool found")
    #sys.exit(1)
    # The tools are returned in the recommended order of usage
    tool = tools[0]
    #print("Will use tool '%s'" % (tool.get_name()))
    # Ex: Will use tool 'libtesseract'
    langs = tool.get_available_languages()
    #print('We will use following languages:')
    #print(', '.join(langs))
    language = 'eng'
    dic = {'file': '-'}
    for l in langs:
        dic[l] = '-'
    with open('passpa.txt', 'r') as rpass:
        imagefile = rpass.readline().rstrip('\n')
        uploaded_file_url = rpass.readline().rstrip('\n')
        result_file_url = rpass.readline().rstrip('\n')
        #recog_res = data_helpers.recog_crop(imagefile, language, dic, tool)
        recog_res = data_helpers.ext_txt(imagefile, language, dic, tool)
        recog_res = data_helpers.clean_str(recog_res)
        with open('single_rec.txt', 'w') as wres:
          wres.write(recog_res)
        return render(request, 'core/recognize.html', {'recognition':recog_res,
        'uploaded_file_url': uploaded_file_url, 'result_file_url': result_file_url})


def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        res_filename = 'res_' + filename
        filepath = os.path.join(fs.location, filename)
        uploaded_file_url = fs.url(filename)
        result_file_url = fs.url(res_filename)
        with open('passpa.txt', 'w') as wpass:
          wpass.write(filepath + '\n')
          wpass.write(uploaded_file_url + '\n')
          wpass.write(result_file_url + '\n')
        
        cropimage.detection(filepath)
        #print (res_dir)
        return render(request, 'core/simple_upload.html', {
            'uploaded_file_url': uploaded_file_url, 'result_file_url': result_file_url,
            'filename': filename})
    return render(request, 'core/simple_upload.html')


def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'core/model_form_upload.html', {
        'form': form
    })
