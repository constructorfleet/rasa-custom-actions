from typing import Dict, Text, Any, List
import os

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

import logging
import requests

_LOGGER = logging.getLogger(__name__)

PERSON_SLOT = 'person'
LOCATION_SLOT = 'location'


class ActionLocatePerson(Action):

    def __init__(self):
        self.bearer_token = os.environ['HOME_ASSISTANT_TOKEN']

    def name(self) -> Text:
        return "action_locate_person"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        person = tracker.get_slot(PERSON_SLOT)

        _LOGGER.warning("Making request")

        response = requests.get(
            f"https://automation.prettybaked.com/api/states/person.{person}",
            headers={
                "Authorization": f"Bearer {self.bearer_token}"
            }
        )

        try:
            response.raise_for_status()
        except requests.HTTPError as err:
            _LOGGER.error(f"ERROR {err}")
            dispatcher.utter_message(text="Heart of Gold does not seem to be responding")
            return []

        location = response.json().get('state', None)

        if not location:
            dispatcher.utter_message(template="utter_locate_failed")
            return []
        else:
            tracker.slots[LOCATION_SLOT] = location
            dispatcher.utter_message(template="utter_locate_success")
            return []
