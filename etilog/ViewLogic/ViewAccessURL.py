'''
Created on23.08.19

@author: daim
'''
import csv

from etilog.ViewLogic.ViewDatetime import get_now

from pywebcopy import save_webpage, WebPage, config
import pdfkit
from  bs4 import BeautifulSoup
#from mercury_parser.client import MercuryParser
from readabilipy import simple_json_from_html_string
import requests

from etilog.models import ImpactEvent

import os
#in order to find wkhtmltopdf executable
os.environ['PATH']='/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin'


def check_ifexist():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    folder_s = 'created_pdf'
    spath = os.path.join(base_dir, folder_s)

    q_ie = ImpactEvent.objects.all()
    error_list = []
    for ie in q_ie:
        if ie.source_url:    
            ie_id = ie.id
            file_name = 'imp_event_' + str(ie_id) + '.pdf'
            file_path = os.path.join(spath, file_name)
            if os.path.exists(file_path) == False:
                error_list.append(ie_id)
    return error_list
            
def parse_url_readabilipy():
    def save_ie(ie, parse_nr):
        ie.result_parse_html = parse_nr
        ie.save()
    #q_ie = ImpactEvent.objects.all()
    #filter impevs which already have article_text
    
    
    #todo_li = [0, 4] #ConnErr: also if no internet connection
    todo_li = [8, 9]
    q_ie =  ImpactEvent.objects.filter(result_parse_html__in = todo_li
                                        ).exclude(source_url__isnull = True
                                        ).exclude(source_url__exact = '')
    #for statistics
    #q_ie =  ImpactEvent.objects.exclude(source_url__isnull = True).exclude(source_url__exact = '')
    q_ie = q_ie
    
    now = get_now()
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    folder_s = 'created_html'
    spath = os.path.join(base_dir, folder_s)


    print('remaining impevs: ', len(q_ie))
    for ie in q_ie:
    #for ie in q_ie.filter(id__in = idlist):
        #if 1 == 1:
        try:
            parse_res = 1 
            ieid = ie.id 
            
            print ('startparsing ', ieid)
            url = ie.source_url  
            try:  
                response = requests.get(url, timeout = 5)
            except requests.exceptions.ConnectionError:                              
                save_ie(ie, 4)
                continue
            except TimeoutError:                              
                save_ie(ie, 7)
                continue

            if 'pdf' in url[-4:]:
                save_ie(ie, 3)
                continue
            
                
            # Extracting the source code of the page.
            html_string = response.text  
            if 'pdf' in html_string.lower()[:5]: #%pdf
                save_ie(ie, 3)
                continue
            #use_readability=True -> Mozilla's Readability.js
            try:
                article = simple_json_from_html_string(html_string, use_readability=True)
            except:
                save_ie(ie, 5)
                continue
            
            html_simple = article.get('content', None)
            #html_plain = article.get('plain_content', None) 
            text_list = article.get('plain_text', None) 
            if text_list == None or text_list == []:
                save_ie(ie, 6)
                continue
            
            stitle = article.get('title', '') 
            
            date = article.get('date', None)
            if date:
                ie.date_text = str(date)[:100]
                
            
            if stitle == None:
                stitle = ''
            txt_str, parse_res = parse_textli(text_list, parse_res)
            text_str = stitle + '\n' + txt_str
            
                       
            ie.article_text = text_str
            ie.article_title = stitle[:150] #max length

            save_ie(ie, parse_res)
            print ('success: ', ieid)
            
            #filename =  'plain_' + str(ie.id) + '.html'            
            #filepath =  os.path.join(spath, filename)
            #with open(filepath, 'w') as f:
            # #   f.write(html_plain)
                
            filename =  'simple_' + str(ie.id) +  '.html'
            filepath =  os.path.join(spath, filename)
            #with open(filepath, 'w') as f:
            #    f.write(html_simple)
                
        except:
        #else:
            save_ie(ie, 2)
            
    filename =  'parse_errors' + '.csv' 
    filepath =  os.path.join(spath, filename)
    err_ids = []
    
    try:
        with open(filepath) as f:
            csvreader = csv.reader(f, delimiter=';')
            next(csvreader)
            for row in csvreader:
                if row[0] == 'id':
                    break
                
                err_ids.append(row[0])        
    except IOError:
        pass
    nonerr_li =[0, 1]
    q_ie_err = ImpactEvent.objects.exclude(result_parse_html__in = nonerr_li).values_list('id', 'result_parse_html')
    
    
    q_ie_nderr = ImpactEvent.objects.filter(updated_at__gt = now
                                            ).exclude(result_parse_html__in = nonerr_li
                                            ).values_list('id', 'result_parse_html')
                                              
    q_ie_nerr = ImpactEvent.objects.exclude(result_parse_html__in = nonerr_li
                                            ).exclude(id__in = err_ids
                                              ).values_list('id', 'result_parse_html')
    rows = [('id', 'errornr')]
    rows.extend(q_ie_err)
    header = ['id', 'errornr-new-date']
    rows.append(header)
    rows.extend(q_ie_nderr)
    header = ['id', 'errornr-new-file']
    rows.append(header)
    rows.extend(q_ie_nerr)
    
        
    with open(filepath, 'w') as f:
        csvwriter = csv.writer(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in rows:
            csvwriter.writerow(row)



def parse_textli(txtdic_li, parse_res):
    txtstr = ''  
    
    #only unique elements
    dubl = set()
    uniq = list() #to keep order a list not a set
    len_max = 0
    for v in txtdic_li:
        x = v['text']
        if x in uniq:
            dubl.add(x)           
        else:
            len_x = len(x)
            if len_x > len_max:
                len_max =  len_x
                max_str = x
            uniq.append(x)
            
    #remove dublicates with a certain length
    len_del = 500
    dubl = set(x for x in dubl if len(x) > len_del)
    txtli = []
    if len(dubl) > 0:
        parse_res = 8
        for x in uniq:
            if x not in dubl:              
                txtli.append(x)
    
    else:
        txtli = uniq    
    len_double = 200
    #txtli = list(uniq - dubl)
    if max_str in txtli:
        k = 0
        k_times = 3
        #check if strings are in max string
        for x in txtli:               
            if x in max_str and len(x) > len_double:
                k += 1
                if k == k_times:
                    parse_res = 10
                    txtli.remove(max_str)
                    break
                
    for row in txtli[:-1]:
        txtstr += row  
        txtstr += '\n' #new line \n
    if len(txtli) > 0:
        txtstr += txtli[-1]
    if len(txtstr) > 50000:
        parse_res = 9
        
    return txtstr, parse_res
        

def parse_url():
    #error_list = check_ifexist()
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    folder_s = 'created_pdf'
    spath = os.path.join(base_dir, folder_s)

    
    q_ie = ImpactEvent.objects.all()
    for ie in q_ie:
        if ie.source_url:     
            get_text_mercury(ie, spath)       
            get_text_bs(ie, spath)
            get_pdf(ie, spath)
        else:
            continue

def get_text_mercury(impactevent, spath):
    #need to install npm and node.js 
    pass

    

    
def get_text_bs(impactevent, spath):
    ie = impactevent
    url = ie.source_url
    
    response = requests.get(url)
    # Extracting the source code of the page.
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')
    
    print (soup.find('body'))
    


def get_pdf(impactevent, spath):
    ie = impactevent
    url = ie.source_url
    #url = 'http://google.com'
    ie_id = ie.id
    file_name = 'imp_event_' + str(ie_id) + '.pdf'
    #file_name = 'test.pdf'
    file_path = os.path.join(spath, file_name)
    try:
        pdfkit.from_url(url, file_path)
    except:
        print ('error: ' + file_name)
    
    
def get_html(impactevent, spath):
    ie = impactevent
    url = ie.source_url
    ie_id = ie.id
    project_name = 'created_html'

    config.setup_config(url, spath)
    config['OVER_WRITE'] = True
    config['LOG_FILE'] = None
    config['project_name'] = project_name
    file_name = 'imp_event_' + str(ie_id)
    config['project_url'] = os.path.join(spath, file_name)  #spath to html -> makes index.html

    wp = WebPage()
    wp.get(url)

    print(wp.file_path)
    #wp.save_complete()
    wp.save_html()
    
def parse_url2():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    kwargs = {'project_name': 'some-fancy-name'}
    folder_s = 'created_pdfs'
    #filename = 'test.pdf'
    spath = os.path.join(base_dir, folder_s)
    save_webpage(
    url='https://weasyprint.readthedocs.io/en/stable/tutorial.html',
    project_folder=spath,
    **kwargs
    )

