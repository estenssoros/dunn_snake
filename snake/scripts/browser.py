import cookielib
import datetime as dt
import os
import re
import shutil
import zipfile

import mechanize
from bs4 import BeautifulSoup
from tqdm import tqdm

base_url = 'https://searchicris.co.weld.co.us/recorder'


def ensure_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


def start_browser():
    br = mechanize.Browser(factory=mechanize.RobustFactory())
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)
    br.set_handle_equiv(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    br.addheaders = [
        ('User-agent',
         'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')
    ]
    url = 'https://searchicris.co.weld.co.us/recorder/web/login.jsp?submit=I+Acknowledge'
    br.open(url)
    br.select_form(nr=1)
    br.form['userId'] = os.environ['WELD_COUNTY_USER_NAME']
    br.form['password'] = os.environ['WELD_COUNTY_PASSWORD']
    br.submit()
    return br

re_num = re.compile(r'([0-9]+)')


def parse_table_soup(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find_all('table', {'id': 'searchResultsTable'})[0]
    trs = table.find_all('tr', {'class': ['even', 'odd']})
    results = []
    for tr in trs:
        anchor = tr.find_all('a')[0]
        link = anchor.get('href')
        while not link.startswith('/') and link:
            link = link[1:]
        doc_id = re_num.findall(anchor.text)[0]
        row = {'doc_id': doc_id, 'link': link}
        results.append(row)
    return results


class SnakeySnake(object):

    def __init__(self, save_path):
        self.br = start_browser()
        self.save_path = os.path.join(save_path, dt.datetime.now().strftime('%Y%m%d_%H%M'))
        ensure_exists(self.save_path)
        self.doc_links = []
        self.pdf_files = []

    def retrieve_document_links(self, doc_ids):
        self.br.select_form(nr=0)
        self.br.form['DocumentNumberID'] = ' '.join(doc_ids)
        req = self.br.submit()
        html = req.read()
        self.doc_links.extend(parse_table_soup(html))

    def download_documents(self):
        for doc in tqdm(self.doc_links):
            url = base_url + doc['link']
            self.br.open(url)
            for link in self.br.links():
                if 'view attachment' in link.text.lower():
                    dst = os.path.join(self.save_path, '{}.pdf'.format(doc['doc_id']))
                    self.pdf_files.append(dst)
                    self.br.retrieve(link.absolute_url, dst)

    def zip_documents(self):
        shutil.make_archive(self.save_path, 'zip', self.save_path)
        shutil.rmtree(self.save_path)

    def retrieve_and_zip_documents(self, doc_ids):
        self.retrieve_document_links(doc_ids)
        self.download_documents()
        self.zip_documents()
        self.kill()

    def kill(self):
        self.br.close()


def main():
    home = os.path.expanduser('~')
    snake = SnakeySnake(home)
    doc_ids = ['255542', '255543', '262389', '109504']
    snake.retrieve_and_zip_documents(doc_ids)
    snake.kill()

if __name__ == '__main__':
    main()
