from typing import Text, Dict, Any, List

import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from actions import _LOGGER
from eddie_actions import HOME_ASSISTANT_TOKEN


def get_current_weather(dispatcher: CollectingDispatcher,
                        tracker: Tracker,
                        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    response = requests.get(
        f"https://automation.prettybaked.com/api/states/weather.dark_sky_hourly",
        headers={
            "Authorization": f"Bearer {self.bearer_token}"
        }
    )
    weather = None

    try:
        response.raise_for_status()
        condition = response.json().get('state', None)
        temperature = response.json().get('attributes', {}).get('temperature', None)
        weather = "it's currently %s and %s" % (
            condition, ("%d degrees" % temperature) if temperature else "")
    except requests.HTTPError as err:
        _LOGGER.error(str(err))
    if not weather:
        dispatcher.utter_message(template="utter_noone_home")
    else:
        dispatcher.utter_message(text=weather)

    return []
