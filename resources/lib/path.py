# -*- coding: utf8 -*-

from xbmcswift2 import Plugin, xbmcaddon, ListItem, xbmc, xbmcgui
import json
import requests

ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')
ADDON_ICON = ADDON.getAddonInfo('icon')
ADDON_NAME = ADDON.getAddonInfo('name')
ADDON_PATH = ADDON.getAddonInfo('path').decode("utf-8")
ADDON_VERSION = ADDON.getAddonInfo('version')
ADDON_DATA_PATH = xbmc.translatePath("special://profile/addon_data/%s" % ADDON_ID).decode("utf-8")


plugin = Plugin()
PLAY_API = "http://1p-1.usgov.club:9998/"
IMAGE_API = "https://raw.githubusercontent.com/yugimaster/infomation.1pondo/master/movies/"
JSON_DATA_URL = "https://raw.githubusercontent.com/yugimaster/infomation.1pondo/master/1pondo.json"


# main entrance
@plugin.route('/')
def index():
    json_query = get_movie_list()
    if not json_query:
        return
    for item in json_query['data']['videos']:
        listitem = {
            'label': item['Title'],
            'path': PLAY_API + item['MovieID'] + "/hls/index.m3u8",
            'icon': IMAGE_API + item['MovieID'] + "/popu.jpg",
            'is_playable': True
        }
        yield listitem


# get local json data
def get_json_data(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
        return data


# get json data from url
def get_url_json(url):
    r = requests.get(url)
    return r.json()


def get_movie_list():
    try:
        json_query = get_url_json(JSON_DATA_URL)
        if json_query and json_query['data']['videos']:
            return json_query
        else:
            return None
    except Exception:
        return get_json_data(ADDON_PATH + "/1pondo.json")
