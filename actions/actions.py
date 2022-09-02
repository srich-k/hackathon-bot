from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import FollowupAction, AllSlotsReset
from rasa.core.actions.forms import FormAction
from rasa_sdk.executor import CollectingDispatcher

static_data = {
               "8008035999": {"name" : "Charan", "address": {1:"Flat 102,3-71/1, Yendada, Endada, Visakhapatnam, Andhra Pradesh 530045, India",2:"Flat No 302, Sunrise Pg, SG Layout,Bengaluru, Karnataka 560035, India",3:"Room 309,CKB Layout, Marathahalli, Bengaluru, Karnataka 560037, India"}}, 
               "9545945338": {"name" : "Piyush", "address": {1:"202 H26,Whitefield - Hoskote Rd, Kannamangala, Bengaluru 560067, India",2:"B3, 305,Green Glen Layout, Bellandur, Bengaluru, Karnataka 560103, India",3:"A304,Nanakramguda Rd, Nanakramguda, Hyderabad, Telangana 500032, India. (Golf View Apartment)"}}, 
               "7073580630": {"name" : "Tanya", "address": {1:"28, Pragati Apartments, 7, west enclave, Pitam Pura,Block C1, West Enclave, Pitam Pura, Delhi, 110034, India",2:"Mapletree Inn,Kaverappa Layout, Kadubeesanahalli, Bengaluru, Karnataka 560103, India",3:"Hotel Mapletree Inn,Kaverappa Layout, Kadubeesanahalli, Bengaluru, Karnataka 560103, India"}}, 
               "7259318319": {"name" : "Ashay", "address": {1: "13281, Tower 13, Floor 28, Prestige Lakeside Habitat,Devasthanagalu, Varthur, Karnataka, India. (Gunjur Village)", 2: "Tamhanes, A1-2 46, 4th Floor, Girijashankar Vihar,Lane Number 6, Meenatai Thakre Nagar, Girija Shankar Vihar, Ganesh Nagar, Karve Nagar, Pune, Maharashtra 411052, India", 3: "Chitre, A3,Kalachowki, Chunabhatti, Sion, Mumbai, Maharashtra 400022, India"}},
               "9886047004": {"name" : "Goda", "address": {1:"Brigade Paramount, B 804,Swamy Vivekananda Road, Rajana Colony, C V Raman Nagar, Bengaluru, Karnataka 560093",2:"Grand Mercure Hotel,Bamboo Bazar, Mysuru, Karnataka, India",3:"937 3rd A Main Road E Block 2nd Stage Rajajinagar,E block, Subramanyanagar,2 State, Rajajinagar, Bengaluru, Karnataka, India"}}, 
               "9637885668": {"name" : "Sanskriti", "address": {1:"Saraswati-2/501, Jalalpur City, Ramjaipal Path, Opposite Gola Road, Off. Bailey Road,FCI Colony, Phase 1, Kaliket Nagar, Patna, Bihar 801503, India",2:"D-1003, Rohan Iksha, Bhoganhalli Road,Bhoganhalli, Bengaluru, Karnataka, India",3:"ICAR-IIWM, Opposite Rail Vihar,Chandrasekharpur, Bhubaneswar, Odisha 751023, India"}}, 
               "9886747160": {"name" : "Jose", "address": {1:"5/2a k x aquene sacred hearts road  t c palya,Unnamed Road, Kithaganur Colony, Bengaluru, Karnataka 560049, India",2:"1 poruthur house   nalanchira,Kerala 695015, India",3:"St John's Hospital Canteen,Koramangala Industrial Layout, Koramangala, Bengaluru, Karnataka 560034, India"}}, 
               "8296867159": {"name" : "Jairaj", "address": {1:"Apartment # 5022, 5th Tower, 2nd Floor,Dattatreya Nagar, Hosakerehalli, Bengaluru, Karnataka 560085, India. (Prestige South Ridge)",2:"Ovum Hospital Banashankari ,3rd Phase, Banashankari 3rd Stage, Banashankari, Bengaluru, Karnataka 560085, India. (Ovum Woman And Child Speciality Hospital)"}}, 
               "7760255118": {"name" : "Hemant", "address": {1:"3061,HAL Central Township, Marathahalli Village, Marathahalli, Bengaluru, Karnataka 560037, India",2:"C - 27, Sector I, Aliganj, Lucknow,C-27, Sector G, Sector-A, Sector L, Aliganj, Lucknow, Uttar Pradesh 226024, India",3:"803,Harizan Colony, DLF Phase 5, Gurugram, Haryana 122002, India. (Bhawna Apartments)"}}
               }

parent_category_buttons = [
    {"title": "Fruits and Vegetables", "payload": '/select_category{"parent_category": "f-and-v"}'},
    {"title": "Snacks", "payload": '/select_category{"parent_category": "snacks"}'},
    {"title": "Beverages", "payload": '/select_category{"parent_category": "beverages"}'},
    {"title": "Stationery", "payload": '/select_category{"parent_category": "stationery"}'},
    {"title": "Others", "payload": '/select_category{"parent_category": "others"}'}
]

f_and_v_buttons = [
    {"title": "🍎 Apple", "payload": '/purchase_item{"item": "apple", "quantifier": "weight"}'},
    {"title": "🍌 Banana", "payload": '/purchase_item{"item": "banana", "quantifier": "weight"}'},
    {"title": "🍅 Tomatoes", "payload": '/purchase_item{"item": "tomato", "quantifier": "weight"}'},
    {"title": "🧅 Onion", "payload": '/purchase_item{"item": "onion", "quantifier": "weight"}'}
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

welcome_buttons = [
    {"title": "Enter details", "payload": '/user_details'},
    {"title": "Explore our catalog", "payload": '/shop_item'}
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
        print(f"IN ACTION: {self.name()}")
        print(f"Parent category is: {parent_category}")
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


class ActionGreetUser(Action):
    def name(self):
        return "action_greet_user"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        message = formulate_message("Hey there 👋, welcome to swiggy", "I am SWIGG-AI your owm personal assistant, I am here to make your ordering journey a breaze. Please choose from the following, you are just a few taps away from having convenience delivered at your doorstep 🚪")
        dispatcher.utter_message(text=message, buttons=welcome_buttons)
        return [FollowupAction("action_listen"), AllSlotsReset()]


class ActionSubmitUserDetails(Action):
    def name(self):
        return "action_submit_user_details"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):
        mobile_no = tracker.get_slot("mobile_no")
        if mobile_no is not None:
            name = static_data.get(mobile_no, {}).get("name")
            if name:
                message = formulate_message(f"Hey {name}! Welcome back to Swiggy", "It is wonderful to see you again, choose from the following")
            else:
                message = formulate_message(f"Wonderful, you are all set to start your order journey, choose from the following")
            dispatcher.utter_message(message)
            return [FollowupAction("action_show_items")]
            

