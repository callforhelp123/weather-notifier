# weather-notifier

Communication Contract:

Request from the microservice by sending a POST request to 71.227.231.40:5000/weather, with a dictionary with the keys "lat" and "lon" (associated with their desired values) encoded into JSON format. Use a response variable to capture the results of the POST request. The weather information will be stored in the .text component of the response variable.

For example:

coords = {"lat": "47.65", "lon": "-122.38"}
url = 'http://127.0.0.1:5000/weather'
response = requests.post(url, json = coords)
print(response.text)

![sequence lol](https://user-images.githubusercontent.com/91185297/218517973-d7797519-01a9-42cd-af98-d10f4f302f98.PNG)
