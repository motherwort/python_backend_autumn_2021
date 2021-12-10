import json
from bs4 import BeautifulSoup
import re
import requests
from urllib.parse import unquote


def get_random_wikipedia_urls(n, output_file='urls.txt'):
    URL = r'https://ru.wikipedia.org/wiki/Служебная:Случайная_страница'
    with open(output_file, 'a') as file:
        for i in range(n):
            url = requests.get(URL).url
            url = unquote(url)
            file.write(url+'\n')
    

def process_text(text):
    pipeline = [
        lambda x: x.lower(),
        lambda x: re.sub(r'\xa0', ' ', x),
        lambda x: re.sub(r'—', ' ', x),
        lambda x: re.sub(r'\n', ' ', x),
        lambda x: re.sub(r'\[(.*?)\]', '', x),
        lambda x: re.sub(r'[^\w -]', '', x),
        lambda x: re.sub(r' {2,}', ' ', x),
        lambda x: re.sub(r' $', '', x),
    ]
    result = text
    for f in pipeline:
        result = f(result)
    return result


def get_k_frequent_words(resp_text, k):
    soup = BeautifulSoup(resp_text, 'html.parser')
    soup = soup.find('div', id='mw-content-text')
    toc = soup.find('div', id="toc")
    if toc:
        toc.decompose()
    footprint = soup.find('div', {'class': 'printfooter'})
    if footprint:
        footprint.decompose()
    text = process_text(soup.text)
    words = text.split()
    counts = {}
    for word in words:
        if len(word) > 1:
            if word in counts:
                counts[word] += 1
            else:
                counts[word] = 1
    sorted_counts = sorted(
        counts.items(), 
        reverse=True, 
        key=lambda item: item[1]
    )
    most_frequent = dict(sorted_counts[:k])
    return most_frequent


if __name__ == '__main__':
    with open('out.txt') as f:
        text = f.read()
        text = re.sub(r' : {[^}]*}\n', '\n', text)
    with open('urls.txt', 'w') as f:
        f.write(text)
    pass
