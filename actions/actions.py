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


from typing import Any, Optional, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet
from collections import Counter
import random


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

        pizzas_complete_order_list = tracker.get_slot(
            "pizzas_complete_order") or []

        pizzas_complete_order_list.append({
            "size": pizza_size,
            "type": pizza_type,
            "amount": pizza_amount
        })

        # reset the slots and add the new pizza to the list
        return [SlotSet("pizza_type", None), SlotSet("pizza_size", None), SlotSet("pizza_amount", None), SlotSet("pizzas_complete_order", pizzas_complete_order_list)]


class ActionPizzaTotalOrder(Action):
    def name(self):
        return 'action_total_order'

    def run(self, dispatcher, tracker, domain):

        side_dishes_list = tracker.get_slot("side_dishes") or []
        pizzas_complete_order_list = tracker.get_slot(
            "pizzas_complete_order") or []

        order_details = " and ".join(
            [f"{pizza['amount']} {pizza['type']} {pizza['size']} size" for pizza in pizzas_complete_order_list])

        if side_dishes_list is not None:
            element_counts = Counter(side_dishes_list)
            side_dishes = [f'{value} {key}' for key,
                           value in element_counts.items()]
            # create the string of side dishes
            total_side_dishes = " and ".join(side_dishes)

            if total_side_dishes != "":
                order_details = order_details + " with " + total_side_dishes

        # dispatcher.utter_message(response="utter_complete_order")

        return [SlotSet("total_order", order_details)]


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

            dispatcher.utter_message(
                text=f"We added {side_dish} to your order")

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
                text=f"We removed {side_dish} from your order")

            element_counts = Counter(side_dishes_list)
            side_dishes = [f'{value} {key}' for key,
                           value in element_counts.items()]
            # create the string of side dishes
            total_side_dishes = " and ".join(side_dishes)
        else:
            dispatcher.utter_message(
                text=f"You have no {side_dish} in your order")

        if not side_dishes_list:
            total_side_dishes = "nothing"

        return [SlotSet("side_dish", side_dish), SlotSet("side_dishes", side_dishes_list), SlotSet("total_side_dishes", total_side_dishes)]


class ActionHandleDetailsOnPromotion(Action):
    def name(self):
        return 'action_handle_details_on_promotion'

    def run(self, dispatcher, tracker, dominan):
        promotion_type = tracker.get_slot("promotion_type")

        if promotion_type == "Duo Party":
            dispatcher.utter_message(
                response="utter_specific_duo_party_promotion")
        elif promotion_type == "Veggie Feast":
            dispatcher.utter_message(
                response="utter_specific_veggie_feast_promotion")
        else:
            dispatcher.utter_message(response="utter_vague_promotion")

        return []


class ActionRecommendPromotion(Action):
    def name(self):
        return 'action_recommend_promotion'

    def run(self, dispatcher, tracker, dominan):
        is_reunion = tracker.get_slot("is_reunion")
        is_vegetarian = tracker.get_slot("is_vegetarian")

        promotion_type = ""

        if is_reunion is not None and is_reunion == 'True':
            dispatcher.utter_message(
                response="utter_recommend_duo_party_promotion")
            promotion_type = "Duo Party"
        elif is_vegetarian is not None and is_vegetarian == 'True':
            dispatcher.utter_message(
                response="utter_recommend_veggie_feast_promotion")
            promotion_type = "Veggie Feast"
        else:
            # case both reunion and vegetarian are None
            dispatcher.utter_message(
                response=f"utter_vague_order_promotion")
            return [SlotSet("promotion_type", None)]

        return [SlotSet("promotion_type", promotion_type)]


class ActionRecommendOnPromotionForm(Action):
    def name(self):
        return 'action_recommend_on_promotion_form'

    def run(self, dispatcher, tracker, domain):
        promotion_type = tracker.get_slot("promotion_type")
        if promotion_type == "Duo Party":
            return [SlotSet("recommend_pizza", "Margherita"), SlotSet("recommend_side_dish", "Chicken Wings")]
        elif promotion_type == "Veggie Feast":  # Veggie Feast
            return [SlotSet("first_pizza_promotion", "Vegetarian"), SlotSet("recommend_side_dish", "French Fries")]
        else:
            # set slots to None
            return [SlotSet("recommend_pizza", None), SlotSet("recommend_side_dish", None), SlotSet("first_pizza_promotion", None), SlotSet("recommend_side_dish", None), SlotSet("second_pizza_promotion", None), SlotSet("second_side_dish", None)]


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
