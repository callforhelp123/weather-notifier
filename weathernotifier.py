import requests
from twilio.rest import Client
import schedule
import time

owm_api_key = "###"
account_sid = '###'
auth_token = '###'
to_phone_number = "+12066973532"
from_phone_number = "+18142575376"
lat = str(47.65)
lon = str(-122.38)

def wind_comparison(weather_data):
    wind = weather_data["current"]["wind_speed"]
    gust = weather_data["hourly"][0]["wind_gust"]
    if wind > gust:
        low_wind = gust
        high_wind = wind
    else:
        low_wind = wind
        high_wind = gust
    return low_wind, high_wind

def extract_current_weather(weather_data):
    temp = weather_data["current"]["temp"]
    clouds = weather_data["current"]["clouds"]
    low_wind, high_wind = wind_comparison(weather_data)
    try:
        current_precip = weather_data["current"]["rain"]["1h"]
    except:
        current_precip = 0.0
    return temp, clouds, low_wind, high_wind, current_precip

def calculate_future_precipitation(weather_data):
    rain_catcher = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
    for i in range(0,7):
        try:
            rain_catcher[i] = weather_data["hourly"][i]["rain"]["1h"]
        except:
            pass
    f1_precip = rain_catcher[0]
    f2_precip = rain_catcher[0]+ rain_catcher[1]
    f8_precip = sum(rain_catcher)
    return f1_precip, f2_precip, f8_precip

def extract_forecasted_weather(weather_data):
    f1_precip, f2_precip, f8_precip = calculate_future_precipitation(weather_data)
    f1_clouds = weather_data["hourly"][0]["clouds"]
    f2_clouds = weather_data["hourly"][1]["clouds"]
    f8_clouds = weather_data["hourly"][7]["clouds"]
    f1_temp = weather_data["hourly"][0]["temp"]
    f2_temp = weather_data["hourly"][1]["temp"]
    f8_temp = weather_data["hourly"][7]["temp"]
    return f1_precip, f2_precip, f8_precip, f1_clouds, f2_clouds, f8_clouds, f1_temp, f2_temp, f8_temp

def send_text_message(message):
    client = Client(account_sid, auth_token)
    # Send the message
    message = client.messages.create(
        body=message,
        from_=from_phone_number,
        to=to_phone_number
    )

def job():

    # Get weather for the lon / lat
    weather_response = requests.get(f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely&appid={owm_api_key}&units=imperial")

    # Extract information from the response
    weather_data = weather_response.json()
    temp, clouds, low_wind, high_wind, current_precip = extract_current_weather(weather_data)
    f1_precip, f2_precip, f8_precip, f1_clouds, f2_clouds, f8_clouds, f1_temp, f2_temp, f8_temp = extract_forecasted_weather(weather_data)

    # Generate message
    message0 = f"Current temp: {temp} F\nRain (-1h): {current_precip} mm\n"
    message1 = f"Clouds: {clouds}% \nWind: {low_wind} to {high_wind} mph\n"
    message2 = f"-----------------------------\n"
    message3 = f"(+1h) {f1_temp} F / {f1_precip} mm rain / {f1_clouds}% clouds\n(+2h) {f2_temp} F / {f2_precip} mm rain / {f2_clouds}% clouds\n(+8h) {f8_temp} F / {f8_precip} mm rain / {f8_clouds}% clouds\n"
    message = message0 + message1 + message2 + message3
    print(message)
    send_text_message(message)
    return

def main_screen_selection():
    print("-------------------------------------------------------------")
    print("Please input the number in parentheses to make your selection.")
    print("(1) Input latitude / longitude")
    print("(2) Input desired times")
    print("(3) Input desired phone number")
    print("(4) Run job once")
    print("(5) Run auto-job (WARNING: Requires force quit)")
    print("(6) Exit")
    print("-------------------------------------------------------------")
    return

def desired_time_input():
    num_choice = int(input("Enter the amount of times you want to receive notifications (integer format): "))
    time_choices = [None] * num_choice
    for i in range(num_choice):
        time_choices[i] = input(f"Enter Time #{i + 1} in 24 hr format (Example: 17:30): ")
    print(f"Your desired times are: {time_choices}. If you see an error, please go back and re-enter the correct values.")
    return time_choices

def scheduled_job():
    try:
        for i in range(len(time_choices)):
            schedule.every().day.at(time_choices[i]).do(job)
            while True:
                schedule.run_pending()
                time.sleep(5)
    except:
        print("ERROR: Please define the desired times with Option (2).")

def change_phone_number():
    print("Please enter in your desired phone number, using the following format: +12066973532\n")
    to_phone_number = str(input("Phone number: "))


finalize = False
print("Welcome to the Weather Notifier 1.0")
while finalize == False:
    main_screen_selection()
    choice = input("Input here: ")
    if str(choice) == '6':
        finalize = True
    elif str(choice) == '1':
        lat = str(input("Latitude: "))
        lon = str(input("Longitude: "))
    elif str(choice) == '2':
        time_choices = desired_time_input()
    elif str(choice) == '3':
        change_phone_number()
    elif str(choice) == '4':
        job()
    elif str(choice) == '5':
        scheduled_job()
