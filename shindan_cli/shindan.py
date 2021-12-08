import random
import time

import requests  # type: ignore
from bs4 import BeautifulSoup as BS  # type: ignore


# type: (int, str, optional[bool]) -> str
def shindan(page_id, shindan_name, wait=False):
    if page_id is int and page_id < 0:
        raise ValueError("invalid page id: %d" % page_id)
    url = 'https://shindanmaker.com/%d' % page_id
    session = requests.session()
    s = session.get(url)
    if s.status_code != 200:
        raise FileNotFoundError(s.status_code)
    source = BS(s.text, features="lxml")
    params = {i['name']: i['value']
              for i in source.find_all('input')[1:4]}
    params['shindanName'] = (shindan_name)
    login = session.post(url, data=params)
    if wait:
        time.sleep(random.uniform(2, 5))
    soup = BS(login.text, features="lxml").find('span', id='shindanResult')
    for i in soup.select("br"):  # type: ignore
        i.replace_with("\n")
    return soup.text  # type: ignore
