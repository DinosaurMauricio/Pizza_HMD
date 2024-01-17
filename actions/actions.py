# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from collections import Counter


class ActionChangeOrder(Action):
    def name(self):
        return 'action_change_order'

    def run(self, dispatcher, tracker, domain):
        pizza_size = tracker.get_slot("pizza_size")
        pizza_type = tracker.get_slot("pizza_type")
        pizza_amount = tracker.get_slot("pizza_amount")

        return [SlotSet("pizza_type", pizza_type), SlotSet("pizza_size", pizza_size), SlotSet("pizza_amount", pizza_amount)]


class ActionPizzaOrderAdd(Action):
    def name(self):
        return 'action_pizza_order_add'

    def run(self, dispatcher, tracker, domain):
        pizza_size = tracker.get_slot("pizza_size")
        pizza_type = tracker.get_slot("pizza_type")
        pizza_amount = tracker.get_slot("pizza_amount")
        if pizza_size is None:
            pizza_size = "standard"
        order_details = str(pizza_amount + " " +
                            pizza_type + " is of "+pizza_size)
        old_order = tracker.get_slot("total_order")
        return [SlotSet("total_order", [order_details]) if old_order is None else SlotSet("total_order", [old_order[0]+' and '+order_details])]


class ActionPizzaTotalOrder(Action):
    def name(self):
        return 'action_total_order'

    def run(self, dispatcher, tracker, domain):
        pizza_size = tracker.get_slot("pizza_size")
        pizza_type = tracker.get_slot("pizza_type")
        pizza_amount = tracker.get_slot("pizza_amount")

        side_dishes_list = tracker.get_slot("side_dishes")

        total_side_dishes = ""

        if side_dishes_list is not None:
            element_counts = Counter(side_dishes_list)
            side_dishes = [f'{value} {key}' for key,
                           value in element_counts.items()]
            # create the string of side dishes
            total_side_dishes = " and ".join(side_dishes)

        order_details = str(pizza_amount + " " +
                            pizza_type + " is of "+pizza_size)

        if total_side_dishes != "":
            order_details = order_details + " with " + total_side_dishes

        return [SlotSet("total_order", order_details)]


class ActionResetPizzaForm(Action):
    def name(self):
        return 'action_reset_pizza_form'

    def run(self, dispatcher, tracker, domain):

        return [SlotSet("pizza_type", None), SlotSet("pizza_size", None), SlotSet("pizza_amount", None)]


class ActionOrderNumber(Action):
    def name(self):
        return 'action_order_number'

    def run(self, dispatcher, tracker, domain):
        name_person = tracker.get_slot("client_name")
        number_person = tracker.get_slot("phone_number")
        order_number = str(name_person + "_"+number_person)
        return [SlotSet("order_number", order_number)]


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

            dispatcher.utter_message(text=f"Adding {side_dish} to your order")

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
        side_dishes_list = tracker.get_slot("side_dishes")

        if side_dishes_list is not None and side_dish in side_dishes_list:
            side_dishes_list.remove(side_dish)
            dispatcher.utter_message(
                text=f"Removing {side_dish} from your order")

            element_counts = Counter(side_dishes_list)
            side_dishes = [f'{value} {key}' for key,
                           value in element_counts.items()]
            # create the string of side dishes
            total_side_dishes = " and ".join(side_dishes)
        else:
            total_side_dishes = "no"
            dispatcher.utter_message(
                text=f"You have no {side_dish} in your order")

        return [SlotSet("side_dish", side_dish), SlotSet("side_dishes", side_dishes_list), SlotSet("total_side_dishes", total_side_dishes)]
