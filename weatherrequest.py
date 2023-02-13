import requests

coords = {"lat": "47.65", "lon": "-122.38"}


url = 'http://127.0.0.1:5000/weather'

response = requests.post(url, json = coords)


print(response)
print(response.text)