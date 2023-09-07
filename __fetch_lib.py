import requests
from bs4 import BeautifulSoup

def get_soup_from_link(url):
    response = requests.get(url, allow_redirects=True, headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64))"})
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup