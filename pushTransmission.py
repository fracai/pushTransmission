#!/usr/local/python/bin/python -OO

import ConfigParser
import sys

import chump
import os


def read_config(config):
    config_path = os.path.join(os.path.dirname(sys.argv[0]), config)
    if not os.path.isfile(config_path):
        sys.exit("Config file not found")
    try:
        with open(config_path, 'r') as config_fp:
            configuration = ConfigParser.ConfigParser()
            configuration.readfp(config_fp)
            return configuration
    except IOError:
        sys.exit("Config file not readable")


def push(torrent_name):
    configuration = read_config("pushover.cfg")
    try:
        api_token = configuration.get("Pushover", "api_token")
        user_key = configuration.get("Pushover", "user_key")
    except ConfigParser.NoSectionError, ConfigParser.NoOptionError:
        sys.exit("Config File missing tokens")

    app = chump.Application(api_token)
    user = app.get_user(user_key)

    title = "Download complete"
    message = torrent_name

    user.send_message(
        message,
        title=title
    )


if 'TR_TORRENT_NAME' not in os.environ:
    sys.exit("Torrent name not set")
else:
    push(os.environ['TR_TORRENT_NAME'])
