# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import FollowupAction
from rasa_sdk.executor import CollectingDispatcher

def formulate_message(*msg_parts):
    message = ""
    for msg_part in msg_parts:
        message += msg_part + "\n"
    return message
    

class ActionShowItems(Action):

    def name(self) -> Text:
        return "action_show_items"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        message = formulate_message("In your area we have the following available on instamart", "Your order will be delivered in 30-40min, rest assured - order away!")
        buttons = []
        
        buttons.append({"title": "Fruits and Vegetables", "payload": '/select_category{"parent_category": "f-and-v"}'})
        buttons.append({"title": "Snacks", "payload": '/select_category{"parent_category": "snacks"}'})
        buttons.append({"title": "Beverages", "payload": '/select_category{"parent_category": "beverages"}'})
        buttons.append({"title": "Stationery", "payload": '/select_category{"parent_category": "stationery"}'})
        buttons.append({"title": "Others", "payload": '/select_category{"parent_category": "others"}'})

        dispatcher.utter_message(text=message, buttons=buttons)
        return [FollowupAction("action_listen")]