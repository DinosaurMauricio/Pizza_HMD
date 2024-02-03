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
        name_person = tracker.get_slot("PERSON")
        number_person = tracker.get_slot("LOC")
        order_number = str(name_person + "_"+number_person)
        return [SlotSet("order_number", order_number)]


class ActionCheckCurrentOrderIsEmpty(Action):
    def name(self):
        return 'action_check_current_order_is_empty'

    def run(self, dispatcher, tracker, domain):
        side_dishes_list = tracker.get_slot("side_dishes") or []
        pizzas_complete_order_list = tracker.get_slot(
            "pizzas_complete_order") or []
        promotions_order_list = tracker.get_slot(
            "complete_promotion_orders") or []

        if not promotions_order_list and not pizzas_complete_order_list and not side_dishes_list:
            return [SlotSet("is_cart_empty", True)]
        else:
            return [SlotSet("is_cart_empty", False)]


class ActionGetRecommendationForUser(Action):
    def name(self):
        return 'action_get_recommendation_for_user'

    def run(self, dispatcher, tracker, domain):

        promotions_order_list = tracker.get_slot(
            "complete_promotion_orders") or []
        is_reunion = tracker.get_slot("is_reunion")
        is_vegetarian = tracker.get_slot("is_vegetarian")
        is_max_promotion_reached = tracker.get_slot("is_max_promotion_reached")
        # number of max promotions is reached so we just recommend other items
        if len(promotions_order_list) == MAX_PROMOTIONS:
            dispatcher.utter_message(
                response="utter_recommendation_max_promotion_reached")
            return [SlotSet("is_max_promotion_reached", True)]

        if not is_max_promotion_reached:
            # no promotions have been ordered
            if not promotions_order_list:
                dispatcher.utter_message(
                    response="utter_recommendation_for_user_no_preference")
            else:
                is_duo_party_promotion_on_costumer_order = "Duo Party" in [
                    promotions['promotion_type'] for promotions in promotions_order_list]
                is_veggie_feast_on_costumer_order = "Veggie Feast" in [
                    promotions['promotion_type'] for promotions in promotions_order_list]

                if is_duo_party_promotion_on_costumer_order:
                    dispatcher.utter_message(
                        response="utter_recommendation_duo_already_ordered")

                elif is_veggie_feast_on_costumer_order:
                    dispatcher.utter_message(
                        response="utter_recommendation_veggie_already_ordered")

                elif is_reunion is not None and is_reunion == 'True':
                    dispatcher.utter_message(
                        response="utter_recommendation_for_user_reunion")
                elif is_vegetarian is not None and is_vegetarian == 'True':
                    dispatcher.utter_message(
                        response="utter_recommendation_for_user_vegetarian")
                elif is_reunion is None and is_vegetarian is None:  # doesn't have reunion or vegetarian
                    dispatcher.utter_message(
                        response="utter_recommendation_for_user_no_preference")

        else:
            # max promotions reached
            dispatcher.utter_message(
                response="utter_recommendation_max_promotion_reached")

        return []
