#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from enum import Enum

class APIQueryType(Enum):
    """
        Enumeration des differentes types de reqûete api
    """
    ARTIST = 'artist'
    ALBUM = 'album'
    TRACK = 'track'

