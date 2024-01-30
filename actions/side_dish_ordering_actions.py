
from typing import Any, Optional, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet
from collections import Counter
import random


class ActionSideDishAdd(Action):
    def name(self):
        return 'action_add_side_dish'

    def run(self, dispatcher, tracker, domain):

        side_dish = tracker.get_slot("side_dish")
        side_dishes_list = tracker.get_slot("side_dishes") or []
        side_dishes_list.append(side_dish)

        if side_dishes_list is not None:
            element_counts = Counter(side_dishes_list)
            side_dishes = [f'{value} {key}' for key,
                           value in element_counts.items()]
            # create the string of side dishes
            total_side_dishes = " and ".join(side_dishes)

            dispatcher.utter_message(
                text=f"I added {side_dish} to your order")

        return [SlotSet("total_side_dishes", total_side_dishes), SlotSet("side_dishes", side_dishes_list)]


class ActionSideDishRemoveAll(Action):
    def name(self):
        return 'action_remove_all_side_dishes'

    def run(self, dispatcher, tracker, domain):
        # remove all side dishes from the list
        return [SlotSet("side_dishes", None), SlotSet("total_side_dishes", None)]


class ActionSideDishRemove(Action):
    def name(self):
        return 'action_remove_side_dish'

    def run(self, dispatcher, tracker, domain):
        side_dish = tracker.get_slot("side_dish")
        side_dishes_list = tracker.get_slot("side_dishes") or []

        if side_dishes_list is not None and side_dish in side_dishes_list:
            side_dishes_list.remove(side_dish)
            dispatcher.utter_message(
                text=f"I removed {side_dish} from your order")
        else:
            dispatcher.utter_message(
                text=f"You have no {side_dish} in your order")

        if not side_dishes_list:
            total_side_dishes = "nothing"
        else:
            element_counts = Counter(side_dishes_list)
            side_dishes = [f'{value} {key}' for key,
                           value in element_counts.items()]
            # create the string of side dishes
            total_side_dishes = " and ".join(side_dishes)

        return [SlotSet("side_dish", side_dish), SlotSet("side_dishes", side_dishes_list), SlotSet("total_side_dishes", total_side_dishes)]
