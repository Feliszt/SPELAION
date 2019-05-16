import requests
import os
import sys

# Get path
execution_path = os.getcwd()

query = ""
i = 0
for arg in sys.argv:
    if(i != 0):
        if(i != 1):
            query += "+"
        query += arg
    i = i + 1

if not os.path.exists(execution_path + "/img/" + query):
    os.makedirs(execution_path + "/img/" + query)

r = requests.get("https://api.qwant.com/api/search/images",
    params={
        'count': 10,
        'q': query,
        't': 'images',
        'safesearch': 0,
        'locale': 'en_US',
        'uiv': 4
    },
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    }
)

response = r.json().get('data').get('result').get('items')
urls = [r.get('media') for r in response]

i = 0
for url in urls:
    with open(execution_path + '/img/' + query + "/" + str(i) + '.jpg', 'wb') as handle:
        response = requests.get(url, stream=True)

        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)
    i = i + 1
