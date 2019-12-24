from typing import Dict, Text, Any, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import logging
import requests

import os

_LOGGER = logging.getLogger(__name__)

PERSON_SLOT = 'person'
LOCK_SLOT = 'lock'

HOME_ASSISTANT_TOKEN = os.environ['HOME_ASSISTANT_TOKEN']


class ActionLocatePerson(Action):

    def __init__(self):
        self.bearer_token = HOME_ASSISTANT_TOKEN

    def name(self) -> Text:
        return "action_locate_person"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        person = next(tracker.get_latest_entity_values(PERSON_SLOT), None)
        # person = tracker.get_slot(PERSON_SLOT)

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
        elif location == "not_home":
            dispatcher.utter_message(template="utter_locate_success_away")
        else:
            dispatcher.utter_message(template="utter_locate_success", location=location)

        return []


class ActionWhoHome(Action):

    def __init__(self):
        self.bearer_token = HOME_ASSISTANT_TOKEN

    def name(self) -> Text:
        return "action_who_home"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        response = requests.get(
            f"https://automation.prettybaked.com/api/states",
            headers={
                "Authorization": f"Bearer {self.bearer_token}"
            }
        )
        people_home = None

        try:
            response.raise_for_status()
            people_home = [
                x['attributes'].get('friendly_name', x['entity_id'].replace('person.', ''))
                for x in response.json() if
                str(x['entity_id']).startswith("person") and x['state'] == 'home']
        except requests.HTTPError as err:
            _LOGGER.error(str(err))

        if not people_home:
            dispatcher.utter_message(template="utter_noone_home")
        else:
            dispatcher.utter_message(template="utter_who_is_home", people=people_home)

        return []
