import struct
import threading
import time

import numpy as np
import pyaudio
import speech_recognition as sr
from MeCab import Tagger

from commander import Commander
from command_dict import (
    ics_dict,
    option_dict,
    direction_dict,
)
from sharedqueue import SharedQueue