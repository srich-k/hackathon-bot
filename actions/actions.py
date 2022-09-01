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
        buttons.append({"title": "vegetables", "payload": "/buy_vegetables"})
        buttons.append({"title": "fruits", "payload": "/buy_fruits"})
        buttons.append({"title": "milk & bread", "payload": "/buy_milk"})
        dispatcher.utter_message(text=message, buttons=buttons)
        return [FollowupAction("action_listen")]