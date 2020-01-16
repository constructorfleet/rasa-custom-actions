import asyncio
from datetime import timedelta
from typing import Dict, Text, Any, List

# from pyprika import Pyprika
from rasa_sdk import Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from . import (
    PAPRIKA_USERNAME,
    PAPRIKA_PASSWORD,
    RECIPE_CATEGORIES_SLOT,
    RECIPE_DURATION_SLOT,
    RECIPE_NAME_SLOT,
    RECIPE_NAME_LIKE_SLOT
)

# pyprika = Pyprika(PAPRIKA_USERNAME, PAPRIKA_PASSWORD, timedelta(hours=24), auto_fetch=True)


def get_a_recipe(dispatcher: CollectingDispatcher,
                 tracker: Tracker,
                 domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    categories = next(tracker.get_latest_entity_values(RECIPE_CATEGORIES_SLOT), None)
    duration = next(tracker.get_latest_entity_values(RECIPE_DURATION_SLOT), None)
    name = next(tracker.get_latest_entity_values(RECIPE_NAME_LIKE_SLOT), None)

    try:
        recipes = []
        # asyncio.get_event_loop().run_until_complete(pyprika.get_recipes(
        #     categories=categories,
        #     duration=duration,
        #     name_like=name
        # ))

        if not recipes or len(recipes) == 0:
            dispatcher.utter_message(template="utter_recipe_not_found")
        else:
            recipe_name = recipes[0].name
            dispatcher.utter_message(template="utter_recipe_name", recipe=recipe_name)
            return [SlotSet(RECIPE_NAME_SLOT, recipe_name)]
    except Exception as err:
        dispatcher.utter_message(template="utter_recipe_failed")

    return []
