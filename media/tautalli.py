import json
import logging
from typing import Text, Dict, Any, List

import requests
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

from . import TAUTALLI_API_KEY, MEDIA_TYPE_SLOT

_LOGGER = logging.getLogger(__name__)

ADDED_COUNT = 5

VALID_MEDIA_TYPES = ["movie", "show"]


def get_recent_media(dispatcher: CollectingDispatcher,
                     tracker: Tracker,
                     domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    media_type = next(tracker.get_latest_entity_values(MEDIA_TYPE_SLOT), None)
    success, recent_media = query_recent_media(media_type)
    _LOGGER.warning(json.dumps(recent_media))

    if not success or not recent_media:
        dispatcher.utter_message(template="utter_media_failed")
    else:
        movies = ", ".join(recent_media.get('movies', []))
        episodes = ", ".join(recent_media.get('episodes', []))
        if not movies and not episodes:
            dispatcher.utter_message(
                text="It appears we haven't added any recent media to our library")
        else:
            message = "We recently added"
            if movies:
                message += f" the movies {movies}"
            if movies and episodes:
                message += " and"
            if episodes:
                message += f" tv episodes {episodes}"

            dispatcher.utter_message(text=message)

    return [SlotSet("media_type", "")]


def query_recent_media(media_type: str = None) -> (bool, Dict[Text, List[str]]):
    _LOGGER.warning(f"Media Type: {media_type}")
    url = f"https://tautulli.home.prettybaked.com//api/v2?apikey={TAUTALLI_API_KEY}" \
        f"&cmd=get_recently_added&count={ADDED_COUNT}"
    if media_type in VALID_MEDIA_TYPES:
        url += f"&media_type={media_type}"
    response = requests.get(
        url,
        headers={
            "Content-Type": "application/json"
        }
    )

    recent_media = {}

    try:
        response.raise_for_status()
        recently_added = response.json().get('response', {}).get('data', {}).get('recently_added', [])
        _LOGGER.warning(json.dumps(recently_added))
        movies = [media['title'] for media in recently_added if
                  media.get('media_type', '') == 'movie' and media.get('title', None)]
        _LOGGER.warning(f"Movies: {json.dumps(movies)}")
        episodes = [f"{media['grandparent_title']} episode {media['title']}"
                    for media in recently_added if
                    media.get('media_type', '') == 'episode'
                    and media.get('title', None) and media.get('grandparent_title', None)]
        _LOGGER.warning(f"Episodes: {json.dumps(episodes)}")
        if movies:
            recent_media['movies'] = movies
        if episodes:
            recent_media['episodes'] = episodes
    except requests.HTTPError as err:
        _LOGGER.error(str(err))

    _LOGGER.warning(json.dumps(recent_media))
    if not recent_media:
        return False, {}
    else:
        return True, recent_media
