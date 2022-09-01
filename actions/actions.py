from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import FollowupAction
from rasa_sdk.executor import CollectingDispatcher

parent_category_buttons = [
    {"title": "Fruits and Vegetables", "payload": '/select_category{"parent_category": "f-and-v"}'},
    {"title": "Snacks", "payload": '/select_category{"parent_category": "snacks"}'},
    {"title": "Beverages", "payload": '/select_category{"parent_category": "beverages"}'},
    {"title": "Stationery", "payload": '/select_category{"parent_category": "stationery"}'},
    {"title": "Others", "payload": '/select_category{"parent_category": "others"}'}
]

f_and_v_buttons = [
    {"title": "Apple", "payload": '/purchase_item{"item": "apple", "quantifier": "weight"}'},
    {"title": "Banana", "payload": '/purchase_item{"item": "banana", "quantifier": "weight"}'},
    {"title": "Pineapple", "payload": '/purchase_item{"item": "pineapple", "quantifier": "weight"}'},
    {"title": "Watermelon", "payload": '/purchase_item{"item": "watermelon", "quantifier": "weight"}'},
    {"title": "Potatoes", "payload": '/purchase_item{"item": "potato", "quantifier": "weight"}'},
    {"title": "Tomatoes", "payload": '/purchase_item{"item": "tomato", "quantifier": "weight"}'},
    {"title": "Onion", "payload": '/purchase_item{"item": "onion", "quantifier": "weight"}'},
]

snack_buttons = [
    {"title": "Lays", "payload": '/purchase_item{"item": "lays", "quantifier": "number"}'},
    {"title": "Nachos", "payload": '/purchase_item{"item": "nachos", "quantifier": "number"}'},
    {"title": "Popcorn", "payload": '/purchase_item{"item": "popcorn", "quantifier": "weight"}'}
]

beverage_buttons = [
    {"title": "mountain dew", "payload": '/purchase_item{"item": "lays", "quantifier": "number"}'},
    {"title": "pepsi", "payload": '/purchase_item{"item": "nachos", "quantifier": "number"}'},
    {"title": "sprite", "payload": '/purchase_item{"item": "popcorn", "quantifier": "weight"}'},
]

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
        dispatcher.utter_message(text=message, buttons=parent_category_buttons)
        return [FollowupAction("action_listen")]


class ActionSelectCategory(Action):
    
    def name(self):
        return "action_select_category"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        parent_category = tracker.get_slot("parent_category")
        if parent_category is None:
            dispatcher.utter_message(text="Could you please choose from the following?", buttons=parent_category_buttons)
            return [FollowupAction("action_listen")]
        parent_categ_str = "Fruits and Vegetables" if parent_category == "f-and-v" else parent_category.capitalize()
        message = formulate_message(f"In {parent_categ_str}", "We have the following available")
        dispatcher.utter_message(text=message, buttons=f_and_v_buttons)
        return [FollowupAction("action_listen")]


class ActionPurchaseItem(Action):

    def name(self):
        return "action_purchase_item"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        parent_category = tracker.get_slot("parent_category")
        if parent_category is None:
            dispatcher.utter_message(text="Could you please choose from the following?", buttons=parent_category_buttons)
            return [FollowupAction("action_listen")]
        parent_categ_str = "Fruits and Vegetables" if parent_category == "f-and-v" else parent_category.capitalize()
        message = formulate_message(f"In {parent_categ_str}", "We have the following available")
        dispatcher.utter_message(text=message, buttons=f_and_v_buttons)
        
        return [FollowupAction("action_listen")]
        
