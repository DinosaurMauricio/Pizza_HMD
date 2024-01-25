
from typing import Any, Optional, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet
from collections import Counter
import random

from actions.general_actions import PIZZA_OPTIONS


def get_pizza_values(tracker):
    pizza_size = tracker.get_slot("pizza_size")
    pizza_type = tracker.get_slot("pizza_type")
    pizza_amount = tracker.get_slot("pizza_amount")

    return pizza_size, pizza_type, pizza_amount


class ActionPizzaTotalOrder(Action):
    def name(self):
        return 'action_total_order'

    def run(self, dispatcher, tracker, domain):

        order_details = ""
        side_dishes_list = tracker.get_slot("side_dishes") or []
        pizzas_complete_order_list = tracker.get_slot(
            "pizzas_complete_order") or []
        promotions_order_list = tracker.get_slot(
            "complete_promotion_orders") or []

        if promotions_order_list is not None:
            # count the number of times the value "Duo Party" appears in the list
            element_counts = Counter(
                [promotion["promotion_type"] for promotion in promotions_order_list])

            # get the number of times the value "Duo Party" appears in the list
            promotions = [f'{value} {key}' for key,
                          value in element_counts.items()]

            order_details = order_details + " and ".join(promotions)

        if pizzas_complete_order_list is not None:
            order_details = order_details + " and ".join(
                [f" {pizza['amount']} {pizza['type']} {pizza['size']} size" for pizza in pizzas_complete_order_list])

        if side_dishes_list is not None:
            element_counts = Counter(side_dishes_list)
            side_dishes = [f'{value} {key}' for key,
                           value in element_counts.items()]
            # create the string of side dishes
            total_side_dishes = " and ".join(side_dishes)

            if total_side_dishes != "":
                order_details = order_details + " with " + total_side_dishes

        return [SlotSet("total_order", order_details)]


class ActionChangeOrder(Action):
    def name(self):
        return 'action_change_order'

    def run(self, dispatcher, tracker, domain):

        pizza_size, pizza_type, pizza_amount = get_pizza_values(tracker)

        return [SlotSet("pizza_type", pizza_type), SlotSet("pizza_size", pizza_size), SlotSet("pizza_amount", pizza_amount)]


class ActionPizzaOrderAdd(Action):
    def name(self):
        return 'action_pizza_order_add'

    def run(self, dispatcher, tracker, domain):

        pizza_size, pizza_type, pizza_amount = get_pizza_values(tracker)

        pizzas_complete_order_list = tracker.get_slot(
            "pizzas_complete_order") or []

        pizzas_complete_order_list.append({
            "size": pizza_size,
            "type": pizza_type,
            "amount": pizza_amount
        })

        return [SlotSet("pizza_type", None), SlotSet("pizza_size", None), SlotSet("pizza_amount", None), SlotSet("pizzas_complete_order", pizzas_complete_order_list)]


class ValidatePizzaOrderForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_pizza_order_form"

    def validate_pizza_type(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:

        if slot_value not in PIZZA_OPTIONS:
            dispatcher.utter_message(
                response="utter_wrong_pizza_type")
            return {"pizza_type": None}
        else:
            return {"pizza_type": slot_value}

    def validate_pizza_size(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:

        available_pizza_sizes = ["10''", "12''", "14''", "18''"]
        possible_size_words = ["small", "big", "medium", "large"]
        if slot_value not in available_pizza_sizes:
            # verify if the size was really not provided, the message should include a "size" word but might not have been captured
            text_of_last_user_message = tracker.latest_message.get("text")
            for size_word in possible_size_words:
                if size_word in text_of_last_user_message:
                    # Convert size_word to the corresponding pizza size
                    index = possible_size_words.index(size_word)
                    converted_pizza_size = available_pizza_sizes[index]
                    return {"pizza_size": converted_pizza_size}

            # it was not included
            dispatcher.utter_message(
                response="utter_wrong_pizza_size")
            return {"pizza_size": None}
        else:
            return {"pizza_size": slot_value}

    def validate_pizza_amount(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        # nothing to validate but might as well keep it as a placeholder
        return {'pizza_amount', slot_value}
