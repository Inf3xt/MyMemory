import requests
import json

with open('creds.json', 'r') as f:
	data = json.load(f)


class MyMemory:
	def __init__(self):
		self.headers = {
			"X-RapidAPI-Key": data['RapidApi_Key'],
			"X-RapidAPI-Host": data['RapidApi_Host']
		}

	def translate(self, original="Hello World!", from_lang="en", to_lang="es", key=None):
		url = "https://translated-mymemory---translation-memory.p.rapidapi.com/api/get"
		params = {"langpair": f"{from_lang}|{to_lang}", "q": original, "mt": "1", "onlyprivate": "0","de":"a@b.c"}
		if key:
			params['key'] = key
			params['onlyprivate'] = "1"
		r = requests.get(
			url,
			headers=self.headers,
			params=params
		).json()
		return r['responseData']['translatedText']

	def create_key(self):
		url = "https://translated-mymemory---translation-memory.p.rapidapi.com/createkey"
		r = requests.get(
			url,
			headers=self.headers
		).json()
		if r['code'] == 200: return r['key'], r['id'], r['pass']
		return "F"

	def set_contribution(self, key=None, original="Hello World", translation="Ciao mondo!", from_lang="en", to_lang="it"):
		if not key:
			raise ValueError("Parse a key!")
		url = "https://translated-mymemory---translation-memory.p.rapidapi.com/set"
		params = {"seg": original, "tra": translation, "langpair": f"{from_lang}|{to_lang}", "key": key, "de": "a@b.c"}
		r = requests.get(
			url,
			headers=self.headers,
			params=params
		).json()
		if r['responseData'] == "OK" and r['responseStatus'] == 200:
			return r['responseDetails'][0]
		return "F"

to_lang = "ru"
from_lang = "en"
original = "Hello World"


MyMemory = MyMemory()
key, _, _ = MyMemory.create_key()
translation = MyMemory.translate(original, from_lang=from_lang, to_lang=to_lang, key=key)
print(MyMemory.set_contribution(key=key, original=original, translation=translation, from_lang=from_lang, to_lang=to_lang))
