import requests
from datetime import datetime
import os

TODAY = datetime.now().strftime("%d/%m/%Y")
CURRENT_TIME = datetime.now().strftime("%H:%M:%S")
APP_ID = os.environ['APP_ID']
API_KEY = os.environ['API_KEY']

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY
}

exercise_data = {
    "query": input("What exercise did you complete today: "),
    "weight_kg": 65,
    "height_cm": 169,
    "age": 32
}

e_response = requests.post(exercise_endpoint, headers=headers, json=exercise_data)
e_response.raise_for_status()
e_data = e_response.json()

username = os.environ['SHEETY_USERNAME']
password = os.environ['SHEETY_PASSWORD']

sheet_endpoint = "https://api.sheety.co/69ea3f7eb3ff37bf7e48768326cded04/trackWorkouts/workouts"
for exercise in e_data['exercises']:
    sheet_data = {
        "workout": {
            "date": TODAY,
            "time": CURRENT_TIME,
            "exercise": exercise['name'].title(),
            "duration": exercise['duration_min'],
            "calories": exercise['nf_calories']
        }
    }

    s_response = requests.post(sheet_endpoint, json=sheet_data, auth=(username, password))
    s_response.raise_for_status()
    print(s_response.text)
