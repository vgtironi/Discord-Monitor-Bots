import gspread
from oauth2client.service_account import ServiceAccountCredentials

import requests
import re
from bs4 import BeautifulSoup as bs

from pprint import pprint

planilha = "" #NOME DA PLANILHA NO DRIVE


def get_itens():
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open(planilha).sheet1
    # nomes = sheet.col_values(1)
    # del nomes[0]
    # pprint(nomes)
    links = sheet.col_values(2)
    del links[0]
    return links
    # itens = dict(zip(nomes, links)) 
    # return itens

def get_nike(url):
    payload = {
        'referer' : url,
        }
    r = requests.get('https://www.nike.com.br/Snkrs/PdpDependeCaptcha',headers=payload)
    soup = bs(r.text, 'html.parser')

    div = soup.find('ul',{'class':'variacoes-tamanhos__lista'})
    if div is None:
        return 'indisponivel'
    else:
        avaliable_sizes = div.select('li:not([class^=tamanho-desabilitado])')
        sizes_in_stock = re.findall(r'data-tamanho="(.*?)"', str(avaliable_sizes))
        return sizes_in_stock


links = get_itens()
pprint(links)
print()
results = []
for url in links:
    results.append(get_nike(url))

pprint(results)