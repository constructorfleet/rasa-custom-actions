# http://host:port/sabnzbd/api?output=json&apikey=APIKEY
# api?mode=queue&start=START&limit=LIMIT&search=SEARCH
import json
from typing import Dict, Text, Any, List

import logging
import requests

from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher

_LOGGER = logging.getLogger(__name__)

HEALTHY = "healthy"
UNHEALTHY = "unhealthy"

STORAGE_HEALTH_MAP = {
    "0": UNHEALTHY,
    "1": HEALTHY
}


def get_storage_health(dispatcher: CollectingDispatcher,
                       tracker: Tracker,
                       domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    url = 'https://stats.prettybaked.com/api/datasources/pro22%7D)'
    response = requests.get(
        url,
        headers={
            "Accept": "application/json",
            "X-Dashboard-Id": "52",
            "X-Panel-Id": "916",
            "X-Grafana-Org-Id": "1"
        }
    )

    health = None

    try:
        response.raise_for_status()
        return_value = response.json().get('data', {}).get('result', [{}])[0].get('value', [-1])[-1]
        health = STORAGE_HEALTH_MAP.get(return_value, None)
    except requests.HTTPError as err:
        _LOGGER.error(str(err))

    if not health:
        dispatcher.utter_message(template="utter_storage_health_failed")
    else:
        dispatcher.utter_message(template="utter_storage_health", storage_health=health)

    return []
