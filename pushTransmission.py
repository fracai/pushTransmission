#!/usr/local/python/bin/python -OO

import ConfigParser
import httplib
import sys
import urllib

import os


def readConf(confFile):
    configuration = ConfigParser.ConfigParser()
    file = os.path.join(os.path.dirname(sys.argv[0]), confFile)

    if not os.path.isfile(file):
        sys.exit("Config file not found")

    try:
        fp = open(file, "r")
        configuration.readfp(fp)
        fp.close()
    except IOError:
        sys.exit("Config file not readable")

    return configuration


def push(torrentName):
    configuration = readConf("pushover.cfg")
    apiToken = configuration.get("Pushover", "api_token")
    userKey = configuration.get("Pushover", "user_key")

    title = "Download complete"
    message = torrentName

    cx = httplib.HTTPSConnection("api.pushover.net:443")
    cx.request(
        "POST",
        "/1/messages",
        urllib.urlencode({
            "token": apiToken,
            "user": userKey,
            "title": title,
            "message": message
        }),
        {"Content-type": "application/x-www-form-urlencoded"}
    )


if 'TR_TORRENT_NAME' not in os.environ:
    sys.exit("Torrent name not set")
else:
    push(os.environ['TR_TORRENT_NAME'])
