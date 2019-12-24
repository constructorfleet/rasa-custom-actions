from typing import Dict, Text, Any, List
import os

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.executor import CollectingDispatcher

import logging
import requests

_LOGGER = logging.getLogger(__name__)

PERSON_SLOT = 'person'
LOCATE_SUCCESS = 'locate_success'
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

        response = requests.get(
            f"https://automation.prettybaked.com/api/states/person.{str(person).lower()}",
            headers={
                "Authorization": f"Bearer {self.bearer_token}"
            }
        )

        location = None

        try:
            response.raise_for_status()
            location = response.json().get('state', None)
        except requests.HTTPError as err:
            _LOGGER.error(str(err))

        if not location:
            dispatcher.utter_message(template="utter_locate_failed")
        else:
            dispatcher.utter_message(template="utter_locate_success", location=location)

        return []

