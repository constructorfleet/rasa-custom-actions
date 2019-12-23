from typing import Dict, Text, Any, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

import requests


PERSON_SLOT = 'person'
LOCATION_SLOT = 'location'


class ActionLocatePerson(Action):

    def name(self) -> Text:
        return "action_locate_person"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        person = tracker.get_slot(PERSON_SLOT)

        response = requests.get(f"https://automation.prettybaked.com/api/states/person.{person}")

        try:
            response.raise_for_status()
        except requests.HTTPError as err:
            dispatcher.utter_message(text="Heart of Gold does not seem to be responding")
            return []

        location = response.json().get('state', None)

        if not location:
            dispatcher.utter_message(template="utter_locate_failed")
            return []
        else:
            return [SlotSet(LOCATION_SLOT, location)]
