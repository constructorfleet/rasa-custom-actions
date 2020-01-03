import logging
import math

from actions.eddie_actions import HOME_ASSISTANT_TOKEN
from actions.eddie_actions.location import who_is_home, locate_person
from actions.eddie_actions.climate import get_current_weather
from actions.games.guess_a_number import play_guess_a_number
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

_LOGGER = logging.getLogger(__name__)

PERSON_SLOT = 'person'
LOCK_SLOT = 'lock'


def is_float(input):
    if not input:
        return False
    try:
        num = float(input)
    except ValueError:
        return False
    return True


def is_int(input):
    if not input:
        return False
    try:
        num = int(input)
    except ValueError:
        return False
    return True


def round_up_10(x):
    return int(math.ceil(x / 10.0)) * 10


class ActionNumberGuess(Action):

    def name(self) -> Text:
        return "action_guess_number"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return play_guess_a_number(dispatcher,
                                   tracker,
                                   domain)


class ActionLocatePerson(Action):

    def __init__(self):
        self.bearer_token = HOME_ASSISTANT_TOKEN

    def name(self) -> Text:
        return "action_locate_person"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return locate_person(dispatcher,
                             tracker,
                             domain)


class ActionWhoHome(Action):

    def __init__(self):
        self.bearer_token = HOME_ASSISTANT_TOKEN

    def name(self) -> Text:
        return "action_who_home"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return who_is_home(dispatcher,
                           tracker,
                           domain)


class ActionGetCurrentWeather(Action):

    def __init__(self):
        self.bearer_token = HOME_ASSISTANT_TOKEN

    def name(self) -> Text:
        return "action_get_current_weather"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return get_current_weather(dispatcher,
                                   tracker,
                                   domain)
