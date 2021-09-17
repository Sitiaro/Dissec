from bs4 import BeautifulSoup as bs4
from urllib3 import PoolManager
import lxml
from gc import collect as DEL
from certifi import where as certificate
from requests import get as req_get
from tqdm.auto import tqdm
from colorama import Fore, Style
import time, os

def URL_pull(site, macOS=False):

    if macOS:
        http = PoolManager(ca_certs=certificate())
    else:
        http = PoolManager()

    obj = http.request('GET', site)

    info = {
        'status':  int(obj.status),
        'headers': dict(obj.headers),
        'html':    obj.data.decode('utf-8')
    }

    del http, obj
    DEL()
    return info

def REQ_pull(site):
    raw = req_get(site)

    info = {
        'status':  int(raw.status_code),
        'headers': dict(raw.headers),
        'html':    raw.text
    }

    del raw
    DEL()
    return info

class BS4_parser:
    def __init__(self, site=None, html=False, puller=['URLLIB', False]):

        if html == False:
            if type(puller) == list:
                html = URL_pull(site, puller[1])['html']

            else:
                html = REQ_pull(site)['html']

        self.soup = bs4(html, 'lxml')   
        self.html = html
        self.title = self.soup.title.string

    def find_tags(self, tag_type):

        html_found = self.soup.find_all(tag_type)
        return html_found

    def find_id(self, id):

        html_id = self.soup.find(id=id)
        return html_id

    def send_obj(self):

        return self.soup

    def info(self):

        info = {
            'title': self.title,
            'html':  self.html
        }

        return info

inp = input('Enter the website that you want to scrape;(example - www.mega.nz) :: ')
parser = BS4_parser(inp)
get_info = parser.info()
print(Fore.CYAN + Style.BRIGHT + 'Processing..\n')
time.sleep(1)
for k in tqdm(range(10000)):
  print(Fore.CYAN + Style.BRIGHT + ' ', end='\r')
time.sleep(1)
os.system('clear')
time.sleep(1)
print(Fore.WHITE + str(get_info))
