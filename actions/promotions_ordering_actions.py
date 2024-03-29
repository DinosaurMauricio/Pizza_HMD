from typing import Any, Optional, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, FollowupAction
from collections import Counter
import random

from actions.general_actions import PIZZA_OPTIONS, SIDES_OPTIONS, MAX_PROMOTIONS


def get_promotion_values(tracker):
    first_side_dish = tracker.get_slot("first_side_dish_promotion")
    second_side_dish = tracker.get_slot("second_side_dish_promotion")
    first_pizza = tracker.get_slot("first_pizza_promotion")
    second_pizza = tracker.get_slot("second_pizza_promotion")

    return first_pizza, second_pizza, first_side_dish, second_side_dish


class ActionValidatePromotionPosibility(Action):
    def name(self):
        return 'action_validate_promotion_posibility'

    def run(self, dispatcher, tracker, domain):
        number_of_promotions = len(tracker.get_slot(
            "complete_promotion_orders") or [])

        if number_of_promotions == MAX_PROMOTIONS:
            return [SlotSet("is_max_promotion_reached", True),
                    SlotSet("promotion_type", None),
                    SlotSet("is_reunion", None),
                    SlotSet("is_vegetarian", None),
                    SlotSet("first_pizza_promotion", None),
                    SlotSet("recommend_side_dish", None),
                    SlotSet("recommend_pizza", None),
                    SlotSet("second_pizza_promotion", None),
                    SlotSet("second_side_dish_promotion", None),
                    SlotSet("first_side_dish_promotion", None),
                    SlotSet("total_promotion_order", None)]
        else:
            return [SlotSet("is_max_promotion_reached", False)]


class ActionPromotionAdd(Action):
    def name(self):
        return 'action_promotion_add'

    def run(self, dispatcher, tracker, domain):

        first_pizza, second_pizza, first_side, second_side = get_promotion_values(
            tracker)

        promotion_type = tracker.get_slot("promotion_type")
        complete_promotion_orders = tracker.get_slot(
            "complete_promotion_orders") or []

        if promotion_type == "Duo Party":
            complete_promotion_orders.append({
                "promotion_type": promotion_type,
                "first_side_dish_promotion": first_side,
                "first_pizza_promotion": first_pizza,
                "second_pizza_promotion": second_pizza
            })
        else:
            complete_promotion_orders.append({
                "promotion_type": promotion_type,
                "first_side_dish_promotion": first_side,
                "second_side_dish_promotion": second_side,
                "first_pizza_promotion": first_pizza
            })

        return [SlotSet("complete_promotion_orders", complete_promotion_orders)]


class ActionChangePromotionOrderItem(Action):
    def name(self):
        return 'action_change_promotion_item'

    def run(self, dispatcher, tracker, domain):
        first_pizza, second_pizza, first_side_dish, second_side_dish = get_promotion_values(
            tracker)
        promotion_type = tracker.get_slot("promotion_type")

        if promotion_type == "Duo Party":
            return [SlotSet("first_pizza_promotion", first_pizza),
                    SlotSet("second_pizza_promotion", second_pizza),
                    SlotSet("first_side_dish_promotion", first_side_dish)]

        else:  # promotion_type == "Veggie Feast":
            return [SlotSet("first_side_dish_promotion", first_side_dish),
                    SlotSet("second_side_dish_promotion", second_side_dish)]


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

        # if there are already two promotions on the order, we don't recommend any more
        is_max_promotion_reached = tracker.get_slot("is_max_promotion_reached")
        print(is_max_promotion_reached)
        print('hmmm it should be here...')
        if is_max_promotion_reached:
            dispatcher.utter_message(
                response="utter_promotion_limit_reached")
            return []

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

        return [SlotSet("promotion_type", promotion_type), SlotSet("is_reunion", None), SlotSet("is_vegetarian", None)]


class ActionRecommendItems(Action):
    def name(self):
        return 'action_recommend_items'

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
                total_order_promotion += f" includes two {size} {first_pizza_promotion} pizzas and {first_side_dish} as a side dish"
            else:
                total_order_promotion += f" includes one {size} {first_pizza_promotion} pizza, one {size} {second_pizza_promotion} pizza and {first_side_dish} as a side dish"

        # because we don't have a third promotion yet we can just use else
        else:
            first_pizza_promotion = tracker.get_slot("first_pizza_promotion")
            first_side_dish = tracker.get_slot("first_side_dish_promotion")
            second_side_dish = tracker.get_slot("second_side_dish_promotion")
            size = "large"

            if first_side_dish == second_side_dish:
                total_order_promotion += f" includes one {size} {first_pizza_promotion} pizza and two {first_side_dish} as a side dishes"
            else:
                total_order_promotion += f" includes one {size} {first_pizza_promotion} pizza, one {first_side_dish} and {second_side_dish} as side dishes"

        return [SlotSet("total_promotion_order", total_order_promotion)]


class ActonRemovePromotion(Action):
    def name(self):
        return 'action_remove_promotion'

    def run(self, dispatcher, tracker, domain):

        complete_promotion_orders = tracker.get_slot(
            "complete_promotion_orders") or []

        if len(complete_promotion_orders) == 0:
            dispatcher.utter_message(response="utter_no_promotions_to_remove")
            return [SlotSet("complete_promotion_orders", None)]

        promotion_mapping = {'first': 0, 'second': 1}

        promotion_numbering = tracker.get_slot("promotion_numbering")

        if promotion_numbering is None:
            dispatcher.utter_message(response="utter_remove_wrong_promotion")
            return [SlotSet("complete_promotion_orders", None)]

        promotion_to_remove = promotion_mapping.get(promotion_numbering, -1)

        try:
            if promotion_to_remove != -1:
                dispatcher.utter_message(
                    message=f"Okay, I removed your {complete_promotion_orders[promotion_to_remove]['promotion_type']} promotion.")

                complete_promotion_orders.pop(promotion_to_remove)

                if len(complete_promotion_orders) > 0:
                    # if there are still promotions left, in this case index can be 0 because either 0 or 1 was removed so the other one is still there
                    dispatcher.utter_message(
                        text=f"I removed your promotion, you still have {complete_promotion_orders[0]['promotion_type']} on your order.")
                else:
                    dispatcher.utter_message(
                        text=f"You have no more promotions on your order.")

                dispatcher.utter_message(
                    response="utter_promotion_removed_complete")
                return [SlotSet("complete_promotion_orders", complete_promotion_orders)]
        except IndexError:
            dispatcher.utter_message(response="utter_remove_wrong_promotion")

        return []


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


class ActionActivateRecommendedPromotion(Action):
    def name(self):
        return 'action_activate_recommend_promotion_form'

    def run(self, dispatcher, tracker, domain):
        promotion_type = tracker.get_slot("promotion_type")
        is_max_promotion_reached = tracker.get_slot("is_max_promotion_reached")

        if is_max_promotion_reached:
            dispatcher.utter_message(response="utter_promotion_limit_reached")
            return [SlotSet("promotion_type", None)]

        if promotion_type == "Duo Party":
            dispatcher.utter_message(
                response="utter_duo_party_order_start")
            return []
            # return [FollowupAction('duo_party_form')]
        elif promotion_type == "Veggie Feast":
            dispatcher.utter_message(
                response="utter_veggie_feast_order_start")
            return [SlotSet("first_pizza_promotion", "Vegetarian")]
           # return [FollowupAction('veggie_feast_form')]
        else:

            dispatcher.utter_message(response="utter_vague_promotion")
            return [SlotSet("promotion_type", None)]


class ActionIsPromotionTypeQuestionSet(Action):
    def name(self):
        return 'action_is_promotion_type_question_set'

    def run(self, dispatcher, tracker, domain):
        promotion_type_question = tracker.get_slot(
            "promotion_type_question")
        promotion_type = tracker.get_slot("promotion_type")

        print(promotion_type_question, promotion_type)
        # if there was a question about a speciic promotion type, promotion_type_question will be set
        if promotion_type_question is None:
            # we check if promotion_type is set, if it is, it means that the user already ordered a promotion and wants to ask about it such as "what side dishes can i get in this promotion?"
            if promotion_type is not None:
                return [SlotSet("promotion_type_question", promotion_type)]
            # else of coure promotion type is sets and its a vague question

        return []


class ActionRestartPromotionTypeQuestion(Action):
    def name(self):
        return 'action_restart_promotion_type_question'

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("promotion_type_question", None)]
