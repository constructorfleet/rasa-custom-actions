import logging

from eddie_actions.location import ActionWhoHome, ActionLocatePerson
from eddie_actions.climate import ActionGetCurrentWeather
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
