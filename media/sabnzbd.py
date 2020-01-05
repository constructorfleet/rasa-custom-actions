# http://host:port/sabnzbd/api?output=json&apikey=APIKEY
# api?mode=queue&start=START&limit=LIMIT&search=SEARCH
import json
from typing import Dict, Text, Any, List

import logging
import requests

from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher

from . import SABNZBD_API_KEY

_LOGGER = logging.getLogger(__name__)

START = 0
LIMIT = 1000


def get_download_queue_count(dispatcher: CollectingDispatcher,
                             tracker: Tracker,
                             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    url = f"https://sabnzbd.home.prettybaked.com/api?output=json&apikey=APIKEY{SABNZBD_API_KEY}" \
        f"&mode=queue&start={START}&limit={LIMIT}"

    response = requests.get(
        url,
        headers={
            "Content-Type": "application/json"
        }
    )

    count = 0

    try:
        response.raise_for_status()
        _LOGGER.warning(json.dumps(response.json()))
        count = response.json().get('queue', {}).get('noofslots_total', 0)
    except requests.HTTPError as err:
        _LOGGER.error(str(err))
        count = None

    if count is None:
        dispatcher.utter_message(template="utter_media_failed")
    elif count == 0:
        dispatcher.utter_message(text="We are not currently downloading any new media.")
    else:
        dispatcher.utter_message(text=f"It seems we have {count} items in the download queue.")

    return []
