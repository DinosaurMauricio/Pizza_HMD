from typing import Any, Optional, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet
from collections import Counter
import random

from actions.general_actions import PIZZA_OPTIONS, SIDES_OPTIONS


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

        if promotion_type == "Veggie Feast":  # Veggie Feast

            valid_indices = [0, 1]  # 0 - French Fries, 1 - Caprese Salad
            random_index = random.choice(valid_indices)
            random_side = SIDES_OPTIONS[random_index]

            return [SlotSet("first_pizza_promotion", "Vegetarian"), SlotSet("recommend_side_dish", random_side)]
        elif promotion_type == "Duo Party":

            random_pizza = random.choice(PIZZA_OPTIONS)
            random_side = random.choice(SIDES_OPTIONS)

            return [SlotSet("recommend_pizza", random_pizza), SlotSet("recommend_side_dish", random_side)]
        else:
            # set slots to None
            return [SlotSet("recommend_pizza", None),
                    SlotSet("recommend_side_dish", None),
                    SlotSet("first_pizza_promotion", None),
                    SlotSet("recommend_side_dish", None),
                    SlotSet("second_pizza_promotion", None),
                    SlotSet("first_side_dish_promotion", None),
                    SlotSet("second_side_dish_promotion", None)]


class ActionPromotionTotalOrder(Action):
    def name(self):
        return 'action_promotion_total_order'

    def run(self, dispatcher, tracker, domain):
        promotion_type = tracker.get_slot("promotion_type")

        total_order_promotion = ""
        total_order_promotion += promotion_type
        if promotion_type == "Duo Party":
            first_pizza_promotion = tracker.get_slot("first_pizza_promotion")
            second_pizza_promotion = tracker.get_slot("second_pizza_promotion")
            first_side_dish = tracker.get_slot("first_side_dish_promotion")

            size = "medium"

            if first_pizza_promotion == second_pizza_promotion:
                total_order_promotion += f" {promotion_type} includes two {size} {first_pizza_promotion} pizzas and {first_side_dish} as a side dish"
            else:
                total_order_promotion += f" {promotion_type} includes one {size} {first_pizza_promotion} pizza, one {size} {second_pizza_promotion} pizza and {first_side_dish} as a side dish"

        # because we don't have a third promotion yet we can just use else
        else:
            first_side_dish = tracker.get_slot("first_side_dish_promotion")
            second_side_dish = tracker.get_slot("second_side_dish_promotion")
            size = "large"

            if first_side_dish == second_side_dish:
                total_order_promotion += f" {promotion_type} includes one size {first_pizza_promotion} pizza and two {first_side_dish} as a side dishes"
            else:
                total_order_promotion += f" {promotion_type} includes one size {first_pizza_promotion} pizza, one {first_side_dish} and {second_side_dish} as side dishes"

        return [SlotSet("total_promotion_order", total_order_promotion)]


class ActionPromotionReset(Action):
    def name(self):
        return 'action_promotion_reset'

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("promotion_type", None),
                SlotSet("is_reunion", None),
                SlotSet("is_vegetarian", None),
                SlotSet("first_pizza_promotion", None),
                SlotSet("recommend_side_dish", None),
                SlotSet("recommend_pizza", None),
                SlotSet("second_pizza_promotion", None),
                SlotSet("second_side_dish_promotion", None),
                SlotSet("first_side_dish_promotion", None),
                SlotSet("total_promotion_order", None)]
