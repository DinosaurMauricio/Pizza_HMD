from typing import Any, Optional, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet
from collections import Counter
import random

from actions.general_actions import PIZZA_OPTIONS, SIDES_OPTIONS, NOT_AVAILABLE_PIZZAS, NOT_AVAILABLE_SIDES


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

        # check its a valid pizza
        available_pizzas = [pizza.lower() for pizza in PIZZA_OPTIONS]

        if slot_value is None:
            return {"first_pizza_promotion": None}

        pizza = slot_value.lower()
        if pizza not in available_pizzas:
            print(pizza, available_pizzas)
            print('======inside first==========')
            dispatcher.utter_message(
                text="Sorry, we currently don't serve that pizza.")
            return {"first_pizza_promotion": None}
        return {"first_pizza_promotion": slot_value}

    def validate_second_pizza_promotion(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `second_pizza_promotion` value."""
        # check its a valid pizza
        available_pizzas = [pizza.lower() for pizza in PIZZA_OPTIONS]

        if slot_value is None:
            return {"second_pizza_promotion": None}

        domain.update()
        pizza = slot_value.lower()
        if pizza not in available_pizzas:
            print(pizza, available_pizzas)
            print('=======inside second=========')
            dispatcher.utter_message(
                text="Sorry, we currently don't serve that pizza.")
            return {"second_pizza_promotion": None}
        return {"second_pizza_promotion": slot_value}

    def validate_first_side_dish_promotion(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `first_side_dish_promotion` value."""
        # check its a valid side dish
        available_sides = [side_dish.lower() for side_dish in SIDES_OPTIONS]

        if slot_value is None:
            return {"first_side_dish_promotion": None}

        side_dish = slot_value.lower()
        if side_dish not in available_sides:
            dispatcher.utter_message(
                text="Sorry, we currently don't serve that side dish.")
            return {"first_side_dish_promotion": None}
        return {"first_side_dish_promotion": slot_value}
