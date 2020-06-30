import json
import sys
import requests
from typing import TypedDict

PATCHNOTES_URL = 'https://api.valstats.net/PatchNotes/fr-fr/?limit=1&sort=date&dir=DESC'

class Patchnote(TypedDict):
    title: str
    date: str
    text: str

def getPatchnote():
    r = requests.get(PATCHNOTES_URL)
    for data in r.json()['data']['patchnotes']:
        _title = data['title']
        _date = data['date']
        _text = data['text']

    return Patchnote(title = _title, date = _date, text = _text)

if __name__ == '__main__':
    from pprint import pprint
    pprint(getPatchnote())