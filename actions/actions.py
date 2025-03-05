from typing import Any, Text, Dict, List
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionStoreUserInfo(Action):
    def name(self) -> str:
        return "action_store_user_info"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        name = tracker.get_slot("name")
        student_number = tracker.get_slot("student_number")

        print(f"DEBUG: Name slot value -> {name}")  # Debugging slot storage
        print(f"DEBUG: Student Number slot value -> {student_number}")

        if not name:
            dispatcher.utter_message(text="I didn't get your name.")
            return []

        if not student_number:
            dispatcher.utter_message(text="I need your student number to proceed.")
            return []

        dispatcher.utter_message(text=f"Thanks {name}, your student number {student_number} is stored.")
        return []

class ActionGetWeather(Action):
    def name(self) -> str:
        return "action_get_weather"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        city = tracker.get_slot("city")

        print(f"DEBUG: City slot value -> {city}")  # Debugging print

        if not city:
            dispatcher.utter_message(text="I need a city name to check the weather.")
            return []

        api_key = "your_api_key_here"  # Replace with a real API key
        url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"

        response = requests.get(url)
        data = response.json()

        if "current" in data:
            temp = data["current"]["temp_c"]
            condition = data["current"]["condition"]["text"]
            dispatcher.utter_message(text=f"The weather in {city} is {condition} with {temp}°C.")
        else:
            dispatcher.utter_message(text="Sorry, I couldn't fetch the weather.")

        return []
