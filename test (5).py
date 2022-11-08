import requests
import json
fliapi = "https://airlabs.co/api/v9/cities?name=Singapore&api_key=961e45ec-e4c1-4ce8-99ef-c9411dde97e2"
#fliapi = "https://airlabs.co/api/v9/cities?city_code=SIN&api_key=961e45ec-e4c1-4ce8-99ef-c9411dde97e2"
data = requests.get(fliapi).json()
data = data['response']
for i in data:
    if i['name'] == 'Vancouver':
        print(i)
