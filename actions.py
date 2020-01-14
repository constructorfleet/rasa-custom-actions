import logging
import math

from eddie_actions.location import who_is_home, locate_person
from eddie_actions.climate import get_current_weather
from games.guess_a_number import play_guess_a_number
from eddie_actions.device import open_garage, close_garage, lock, unlock

from media.tautalli import get_recent_media
from media.sabnzbd import get_download_queue_count

from network.storage import get_storage_health

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
    def name(self) -> Text:
        return "action_get_current_weather"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return get_current_weather(dispatcher,
                                   tracker,
                                   domain)


class ActionOpenGarage(Action):
    def name(self) -> Text:
        return "action_open_garage"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return open_garage(dispatcher,
                           tracker,
                           domain)


class ActionCloseGarage(Action):
    def name(self) -> Text:
        return "action_close_garage"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return close_garage(dispatcher,
                            tracker,
                            domain)


class ActionUnlock(Action):
    def name(self) -> Text:
        return "action_unlock"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return unlock(dispatcher,
                      tracker,
                      domain)


class ActionLock(Action):
    def name(self) -> Text:
        return "action_lock"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return lock(dispatcher,
                    tracker,
                    domain)


class ActionGetRecentMedia(Action):
    def name(self) -> Text:
        return "action_recent_media"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return get_recent_media(dispatcher,
                                tracker,
                                domain)


class ActionGetDownloadCount(Action):
    def name(self) -> Text:
        return "action_download_count"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return get_download_queue_count(dispatcher,
                                        tracker,
                                        domain)


class ActionGetStorageStatus(Action):
    def name(self) -> Text:
        return "action_storage_status"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return get_storage_health(dispatcher,
                                  tracker,
                                  domain)
