from typing import Any, Optional, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet
from collections import Counter
import random

from actions.general_actions import PIZZA_OPTIONS, SIDES_OPTIONS, NOT_AVAILABLE_PIZZAS, NOT_AVAILABLE_SIDES


class ValidateVeggieFeastForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_veggie_feast_form"

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

        if side_dish not in ["french fries", "caprese salad"]:
            dispatcher.utter_message(
                text="Sorry, we currently don't serve that side dish. You can only get vegetarian side dishes with this promotion.")
            return {"first_side_dish_promotion": None}

        return {"first_side_dish_promotion": slot_value}

    def validate_second_side_dish_promotion(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `second_side_dish_promotion` value."""
        # check its a valid side dish
        available_sides = [side_dish.lower() for side_dish in SIDES_OPTIONS]

        if slot_value is None:
            return {"second_side_dish_promotion": None}

        side_dish = slot_value.lower()
        if side_dish not in available_sides:
            dispatcher.utter_message(
                text="Sorry, we currently don't serve that side dish.")
            return {"second_side_dish_promotion": None}

        if side_dish not in ["french fries", "caprese salad"]:
            dispatcher.utter_message(
                text="Sorry, don't serve that side dish on this promotion. You can only get vegetarian side dishes with this promotion.")
            return {"second_side_dish_promotion": None}

        return {"second_side_dish_promotion": slot_value}
