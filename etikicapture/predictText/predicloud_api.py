import json
import requests
import os


def get_category(res_d, threshold):
    """multi class"""
    # in future, when list: result = [1 if p > threshold else 0 for p in raw_outputs[0]]
    res = res_d['multi']
    names = res_d['multi_n']

    pred_dict_m = {1: 'People',
                   2: 'Animals',
                   3: 'Environment',
                   4: 'Politics',
                   5: 'Products & Services'}
    # control of order
    if pred_dict_m[2] != names[2-1]:
        print('wrong category predict dict')
        return None
    max_val = max(res)
    if max_val > threshold:
        k = res.index(max_val) + 1
        cat_id = k
        cat_name = pred_dict_m[k]
        print('category is', cat_name)
    else:
        cat_id, cat_name = 0, 'No Category Found'
    return cat_id, cat_name


def get_tendency(res_d, threshold=0.3):
    res = res_d['sentiment']
    names = res_d['sentiment_n']

    tend_id_dict = {0: 1,  # id = 1  'negative', #id = 1
                    1: 3,  # id = 3 'controversial'
                    2: 2}  # id = 2 'positive'

    tend_name_dict = {0: 'negative',  # id = 1
                      1: 'controversial',
                      2: 'positive'}
    if tend_name_dict[0] != names[0]:
        print('wrong tendency predict dict')
        return None
    max_val = max(res)
    if max_val > threshold:
        k = res.index(max_val)
        tend_id = tend_id_dict[k]
        tend_name = tend_name_dict[k]
        print('tendency is', tend_name)
    else:
        tend_id = 3
        tend_name = 'controversial'
    return tend_id, tend_name


def analyze_text(text):
    return False  # linode delted 8.12.21
    url = os.getenv('PREDICLOUD_URL')
    apitoken = os.getenv('PREDICLOUD_TOKEN')
    headers = {'apitoken': apitoken}
    response = requests.post(url, headers=headers, json={'text': text}, allow_redirects=False)
    if response.ok is False:
        return False
    res_d = response.json()
    cat_id, cat_name = get_category(res_d, threshold=0.5)
    tend_id, tend_name = get_tendency(res_d)

    predict_d = {'tendency_id': tend_id,
                 'category_id': cat_id,
                 'category_name': cat_name,
                 'tendency_name': tend_name,
                 }
    return predict_d


if __name__ == '__main__':
    from etikiptype1.settings.secrets import PREDICLOUD_TOKEN, PREDICLOUD_URL

    os.environ['PREDICLOUD_TOKEN'] = PREDICLOUD_TOKEN
    os.environ['PREDICLOUD_URL'] = PREDICLOUD_URL
    #os.environ['PREDICLOUD_URL'] = 'http://0.0.0.0:80/predict'

    txt = 'child labour'
    analyze_text(txt)


