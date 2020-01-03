import logging
import math

from eddie_actions import HOME_ASSISTANT_TOKEN
from eddie_actions.location import who_is_home, locate_person
from eddie_actions.climate import get_current_weather
import random
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
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
        min_number = int(tracker.get_slot("number_guess_min"))
        max_number = int(tracker.get_slot("number_guess_max"))
        number = tracker.get_slot("number_guess")

        actual_number = random.randint(min_number, max_number)

        if not is_int(number):
            dispatcher.utter_message(text="That's not a number!")
            return [SlotSet("number_guessed", False)]
        if int(number) < min_number or int(number) > max_number:
            dispatcher.utter_message(text="You might be hard of hearing, I said between %d and %d" % (min_number, max_number))
            return [SlotSet("number_guessed", False)]
        if actual_number == int(number):
            dispatcher.utter_message(text="In all my circuits, I never would have predicted you would guess that correctly!")
        else:
            dispatcher.utter_message(text="Silly human, the number I selected was %d" % actual_number)

        return [SlotSet("number_guessed", True)]


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
