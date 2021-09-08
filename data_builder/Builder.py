import requests
import re
import unicodedata
from bs4 import BeautifulSoup
import json


class Builder:

    def __init__(self):
        self.words = []

    def collectWords(self):
        with open('Data/fr.txt', 'r') as dictionnary:
            self.words = dictionnary.read()
            self.words = [w for w in self.words.splitlines(
            ) if re.sub("[a-zA-Zàéèêâùôûî]+", '', w) == '']
        with open('Data/fr.json', 'w') as json_file:
            data = []
            for word in self.words:
                data.append({
                    'word': word,
                    'pronunciation': '',
                    'definition': ''
                })
            json.dump(data, json_file, ensure_ascii=False)

    def getLocutions(self):
        """
        Add locutions in json file from https://fr.wiktionary.org/
        """
        with open('Data/fr.json') as json_file:
            data = json.load(json_file)
            l = len(data)
            for i, d in enumerate(data):
                print(str(i) + "/" + str(l) + "  ---  " + str(int((i/(l+1))*100))+"%")
                content = self.getContent("https://fr.wiktionary.org/wiki/", d['word'])
                if content is not None:
                    d['pronunciation'] = re.sub("<.*?>", "", str(content.findAll('span', {'title': 'Prononciation API'})))
                
            json.dump(data, json_file, ensure_ascii=False)

    def getDefinitions(self):
        """
        Add definitions in json file from https://fr.larousse.fr/
        """
        with open('Data/fr.json') as json_file:
            data = json.load(json_file)
            for d in data:
                content = self.getContent('https://www.larousse.fr/dictionnaires/francais/', d['word'])
                if content is not None:
                    d['definition'] = re.sub("<.*?>", "", str(content.findAll('li', {'class': 'DivisionDefinition'})))
                    print(d)
                
            json.dump(data, json_file, ensure_ascii=False)

    def getContent(self, url, word):
        completeUrl = url + word
        rq = requests.get(url=completeUrl)
        if rq.status_code != 200:
            print("Status code return an error")
            return None
        return BeautifulSoup(rq.text, 'html.parser')
