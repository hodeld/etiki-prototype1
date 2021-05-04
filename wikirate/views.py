import requests
from django.shortcuts import render


def get_wr_data(request):
    companies = []
    for c in companies:
        metric_name = ''
        company_name = ''
        get_answer(metric_name, company_name)


def get_answer(metric_name, company_name):
    url = f'https://wikirate.org/{metric_name}+{company_name}.json'  # returns all answers (all years)
    response = requests.get(url)
    if response.ok is False:
        return False
    res_d = response.json()
    answers = res_d['items']
    for a in answers:
        a_id = a['id']
        a_value = a['value']
        year = a['year'] # 4 digits
        print(a_id, a_value, year)