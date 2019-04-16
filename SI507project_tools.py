# -*- coding: utf-8 -*-

import requests, requests_cache
import json


#https://chroniclingamerica.loc.gov/search/titles/results/?terms=michigan&format=json&page=5

requests_cache.install_cache('chroniclingamerica')

baseurl = "https://chroniclingamerica.loc.gov/search/titles/results/"

params={"format":"json","page":1}

first_result = requests.get(baseurl,params).json()

with open('test_string.txt',"w",encoding="utf8",newline="") as testfile:
    testfile.write(json.dumps(first_result))

print(first_result)
