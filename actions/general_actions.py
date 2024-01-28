from typing import Any, Optional, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet
from collections import Counter
import random


PIZZA_OPTIONS = ["Hawaii", "Funghi",
                 "Pepperoni", "Margherita", "Vegetarian"]
SIDES_OPTIONS = ["French Fries", "Caprese Salad",
                 "Chicken Wings", "Bacon Jalapeno"]

NOT_AVAILABLE_PIZZAS = ["Quattro Formaggi", "Diavola", "Capricciosa", "Prosciutto e Funghi",
                        "BBQ Chicken", "Americana", "Supreme", "Meat Lovers"]

NOT_AVAILABLE_SIDES = ["Onion Rings", "Garlic Bread",
                       "Mozzarella Sticks", "Caesar Salad", "Sweet Potato Fries"]

MAX_PROMOTIONS = 2


class ActionOrderNumber(Action):
    def name(self):
        return 'action_order_number'

    def run(self, dispatcher, tracker, domain):
        name_person = tracker.get_slot("client_name")
        number_person = tracker.get_slot("phone_number")
        order_number = str(name_person + "_"+number_person)
        return [SlotSet("order_number", order_number)]
