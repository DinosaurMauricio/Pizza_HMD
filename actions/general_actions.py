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


class ActionOrderNumber(Action):
    def name(self):
        return 'action_order_number'

    def run(self, dispatcher, tracker, domain):
        name_person = tracker.get_slot("client_name")
        number_person = tracker.get_slot("phone_number")
        order_number = str(name_person + "_"+number_person)
        return [SlotSet("order_number", order_number)]


class ValidateDuoPartyForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_duo_party_form"

    def validate_first_pizza_promotion(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `first_pizza_promotion` value."""

        # If the name is super short, it might be wrong.
        name = ""
        print('name is ', name)
        if len(name) == 0:
            dispatcher.utter_message(text="That must've been a typo.")
            return {"first_pizza_promotion": None}
        return {"first_pizza_promotion": name}

    def validate_second_pizza_promotion(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `second_pizza_promotion` value."""

        # If the name is super short, it might be wrong.
        name = ""
        print('name is ', name)
        if len(name) == 0:
            dispatcher.utter_message(text="That must've been a typo.")
            return {"second_pizza_promotion": None}
        return {"second_pizza_promotion": name}

    def validate_first_side_dish_promotion(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `first_side_dish_promotion` value."""

        # If the name is super short, it might be wrong.
        name = ""
        print('name is ', name)
        if len(name) == 0:
            dispatcher.utter_message(text="That must've been a typo.")
            return {"first_side_dish_promotion": None}
        return {"first_side_dish_promotion": name}
