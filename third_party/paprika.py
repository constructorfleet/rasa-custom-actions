from typing import Dict, Text, Any, List

from pyprika import Pyprika
from rasa_sdk import Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from . import (
    RECIPE_CATEGORIES_SLOT,
    RECIPE_DURATION_SLOT,
    RECIPE_NAME_SLOT,
    RECIPE_NAME_LIKE_SLOT
)


def get_a_recipe(client: Pyprika,
                 dispatcher: CollectingDispatcher,
                 tracker: Tracker,
                 domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    categories = next(tracker.get_latest_entity_values(RECIPE_CATEGORIES_SLOT), None)
    duration = next(tracker.get_latest_entity_values(RECIPE_DURATION_SLOT), None)
    name = next(tracker.get_latest_entity_values(RECIPE_NAME_LIKE_SLOT), None)

    try:
        recipes = client.get_recipes(
            categories=categories,
            duration=duration,
            name_like=name
        )

        recipe_name = recipes[0].name if recipes and len(recipes) > 0 else None
        if not recipe_name:
            dispatcher.utter_message(template="utter_recipe_not_found")
        else:
            dispatcher.utter_message(template="utter_recipe_name", recipe=recipe_name)
        return [SlotSet(RECIPE_NAME_SLOT, recipe_name)]
    except Exception as err:
        dispatcher.utter_message(template="utter_recipe_failed")

    return []
