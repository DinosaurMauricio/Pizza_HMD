
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

        return [SlotSet("side_dish", None), SlotSet("total_side_dishes", total_side_dishes), SlotSet("side_dishes", side_dishes_list), SlotSet("is_side_dish_total_empty", False)]


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
        side_was_in_list_but_removed = False
        if side_dishes_list is not None and side_dish in side_dishes_list:
            side_dishes_list.remove(side_dish)
            side_was_in_list_but_removed = True

        # the list removed an item but now it's empty
        if side_was_in_list_but_removed and not side_dishes_list:
            return [SlotSet("was_requested_side_dish_in_order", side_was_in_list_but_removed), SlotSet("side_dish", None),
                    SlotSet("side_dishes", side_dishes_list), SlotSet("is_side_dish_total_empty", True)]

        # the list is now empty but the side was never in the order
        if not side_dishes_list and not side_was_in_list_but_removed:
            return [SlotSet("was_requested_side_dish_in_order", side_was_in_list_but_removed), SlotSet("side_dishes", side_dishes_list), SlotSet("is_side_dish_total_empty", True)]
        else:
            # the list still has elements we have to check the was it was in the list

            element_counts = Counter(side_dishes_list)
            side_dishes = [f'{value} {key}' for key,
                           value in element_counts.items()]
            # create the string of side dishes
            total_side_dishes = " and ".join(side_dishes)
            return [SlotSet("was_requested_side_dish_in_order", side_was_in_list_but_removed), SlotSet("side_dish", None),
                    SlotSet("side_dishes", side_dishes_list), SlotSet("total_side_dishes", total_side_dishes), SlotSet("is_side_dish_total_empty", False)]
