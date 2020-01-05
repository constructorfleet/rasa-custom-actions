from typing import Dict, Text, Any, List

import requests
import logging

from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher

from . import HOME_ASSISTANT_TOKEN

_LOGGER = logging.getLogger(__name__)
DEVICE_SLOT = 'device'


def turn_on_device(dispatcher: CollectingDispatcher,
                   tracker: Tracker,
                   domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    device = next(tracker.get_latest_entity_values(DEVICE_SLOT), None)
    response = requests.post(
        f"https://automation.prettybaked.com/api/services/homeassistant/turn_on",
        headers={
            "Authorization": f"Bearer {HOME_ASSISTANT_TOKEN}"
        },
        json={
            "entity_id": ""
        }
    )

    try:
        response.raise_for_status()
    except requests.HTTPError as err:
        _LOGGER.error(str(err))
        dispatcher.utter_message(template="utter_device_failed")
        return []

    dispatcher.utter_message(template="utter_turned_on")

    return []


def turn_off_device(dispatcher: CollectingDispatcher,
                    tracker: Tracker,
                    domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    device = next(tracker.get_latest_entity_values(DEVICE_SLOT), None)
    response = requests.post(
        f"https://automation.prettybaked.com/api/services/homeassistant/turn_off",
        headers={
            "Authorization": f"Bearer {HOME_ASSISTANT_TOKEN}",
            "Content-Type": "application/json"
        },
        json={
            "entity_id": ""
        }
    )

    try:
        response.raise_for_status()
    except requests.HTTPError as err:
        _LOGGER.error(str(err))
        dispatcher.utter_message(template="utter_device_failed")
        return []

    dispatcher.utter_message(template="utter_turned_off")

    return []


def lock(dispatcher: CollectingDispatcher,
         tracker: Tracker,
         domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    response = requests.post(
        f"https://automation.prettybaked.com/api/services/lock/lock",
        headers={
            "Authorization": f"Bearer {HOME_ASSISTANT_TOKEN}",
            "Content-Type": "application/json"
        },
        json={
            "entity_id": "lock.front_door"
        }
    )

    try:
        response.raise_for_status()
    except requests.HTTPError as err:
        _LOGGER.error(str(err))
        dispatcher.utter_message(template="utter_device_failed")
        return []

    dispatcher.utter_message(template="utter_locked")

    return []


def unlock(dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    response = requests.post(
        f"https://automation.prettybaked.com/api/services/lock/unlock",
        headers={
            "Authorization": f"Bearer {HOME_ASSISTANT_TOKEN}",
            "Content-Type": "application/json"
        },
        json={
            "entity_id": "lock.front_door"
        }
    )

    try:
        response.raise_for_status()
    except requests.HTTPError as err:
        _LOGGER.error(str(err))
        dispatcher.utter_message(template="utter_device_failed")
        return []

    dispatcher.utter_message(template="utter_unlocked")

    return []


def open_garage(dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    response = requests.post(
        f"https://automation.prettybaked.com/api/services/cover/open_cover",
        headers={
            "Authorization": f"Bearer {HOME_ASSISTANT_TOKEN}",
            "Content-Type": "application/json"
        },
        json={
            "entity_id": "cover.garage_door_2"
        }
    )

    try:
        response.raise_for_status()
    except requests.HTTPError as err:
        _LOGGER.error(str(err))
        dispatcher.utter_message(template="utter_device_failed")
        return []

    dispatcher.utter_message(template="utter_open_garage")

    return []


def close_garage(dispatcher: CollectingDispatcher,
                 tracker: Tracker,
                 domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    response = requests.post(
        f"https://automation.prettybaked.com/api/services/cover/close_cover",
        headers={
            "Authorization": f"Bearer {HOME_ASSISTANT_TOKEN}",
            "Content-Type": "application/json"
        },
        json={
            "entity_id": "cover.garage_door_2"
        }
    )

    try:
        response.raise_for_status()
    except requests.HTTPError as err:
        _LOGGER.error(str(err))
        dispatcher.utter_message(template="utter_device_failed")
        return []

    dispatcher.utter_message(template="utter_closed_garage")

    return []
