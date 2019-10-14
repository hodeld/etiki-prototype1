'''
Created on23.08.19

@author: daim
'''

from readabilipy import simple_json_from_html_string
import requests

from etilog.models import ImpactEvent

            
def parse_url_all():
    def save_ie(ie, parse_nr):
        ie.result_parse_html = parse_nr
        ie.save()
    
    todo_li = [0, 4] #ConnErr: also if no internet connection
    q_ie =  ImpactEvent.objects.filter(result_parse_html__in = todo_li
                                        ).exclude(source_url__isnull = True
                                        ).exclude(source_url__exact = '')
       
    print('remaining impevs: ', len(q_ie))
    for ie in q_ie:
        parse_url(ie)
            
def parse_url(ie):
    def save_ie(ie, parse_nr):
        ie.result_parse_html = parse_nr
        ie.save()

    try:
        parse_res = 1 
        ieid = ie.id 
        
        print ('startparsing ', ieid)
        url = ie.source_url  
        try:  
            response = requests.get(url, timeout = 5)
        except requests.exceptions.ConnectionError:                              
            save_ie(ie, 4)
            return
        except TimeoutError:                              
            save_ie(ie, 7)
            return

        if 'pdf' in url[-4:]:
            save_ie(ie, 3)
            return
                        
        # Extracting the source code of the page.
        html_string = response.text  
        if 'pdf' in html_string.lower()[:5]: #%pdf
            save_ie(ie, 3)
            return
        #use_readability=True -> Mozilla's Readability.js
        article = simple_json_from_html_string(html_string, use_readability=True)
        try:
            article = simple_json_from_html_string(html_string, use_readability=True)
        except:
            save_ie(ie, 5)
            return
        
        html_simple = article.get('content', None)
        text_list = article.get('plain_text', None) 
        if text_list == None or text_list == []:
            save_ie(ie, 6)
            return
        
        stitle = article.get('title', '') 
        
        date = article.get('date', None)
        if date:
            ie.date_text = str(date)[:100]
                    
        if stitle == None:
            stitle = ''
        txt_str, parse_res = parse_textli(text_list, parse_res)
        text_str = stitle + '\n' + txt_str
        len_n = len(text_str)
        
        oldtext =  ie.article_text
        if oldtext:
            len_o = len(oldtext)
            if abs((len_n-len_o)/len_o) > .1:
                print('great difference')    
            if parse_res == 8 or    parse_res == 10  :
                print ('still double stuff')
        
        #ie.article_text = text_str
        ie.article_html = html_simple
        ie.article_title = stitle[:150] #max length

        save_ie(ie, parse_res)
        print ('success: ', ieid)
            
    except:
        save_ie(ie, 2)

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
        

