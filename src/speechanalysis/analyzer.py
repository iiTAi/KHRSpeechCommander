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
from content_field import ContentField


SAMPLE_RATE = 16000
FRAME_SIZE = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
DEVICE_INDEX = 1

AMP_THRESHOLD = 2000
LOW_COUNT_MAX = 3
FINISH_KEYWORD = "終了"

PRINT_INTERVAL = 0.05


class __StateManager:
    def __init__(self):
        self.is_recording = True
        self.is_recognizing = True
        self.is_printing = True
        self.is_analyzing = True

    def start_processes(self):
        self.is_recording = True
        self.is_recognizing = True
        self.is_printing = True
        self.is_analyzing = True

    def stop_processes(self):
        self.is_recording = False
        self.is_recognizing = False
        self.is_printing = False
        self.is_analyzing = False


def init() -> None:
    global commander

    commander = Commander()
    commander.init_connection()


def run(cf: ContentField) -> None:
    global commander
    global s_queue
    global state

    s_queue = SharedQueue()
    state = __StateManager()

    recording_thread = threading.Thread(
        target=__recording_process,
        args=(s_queue, state,))
    recording_thread.start()

    recognition_thread = threading.Thread(
        target=__recognition_process,
        args=(s_queue, state,))
    recognition_thread.start()

    printing_thread = threading.Thread(
        target=__printing_process,
        args=(s_queue, state, cf,))
    printing_thread.start()

    analyzing_thread = threading.Thread(
        target=__analyzing_process,
        args=(s_queue, commander, state,))
    analyzing_thread.start()

    state.start_processes()

    recording_thread.join()
    recognition_thread.join()
    printing_thread.join()
    analyzing_thread.join()


def stop() -> None:
    global commander
    global state
    
    state.stop_processes()
    commander.disconnect()


def __recording_process(
        s_queue: SharedQueue,
        state: __StateManager,) -> None:
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=SAMPLE_RATE,
        input=True,
        frames_per_buffer=FRAME_SIZE,
        input_device_index=DEVICE_INDEX,)
    
    is_speaking = False
    low_count = 0
    signal = b''

    stream.start_stream()
    while stream.is_active() and state.is_recording:
        signal_buffer = stream.read(FRAME_SIZE)

        max_amp = np.max(np.abs(struct.unpack(f"{FRAME_SIZE}h", signal_buffer)))
        if max_amp > AMP_THRESHOLD:
            if not is_speaking:
                is_speaking = True
            low_count = 0
            signal += signal_buffer
        elif is_speaking:
            if low_count < LOW_COUNT_MAX:
                low_count += 1
                signal += signal_buffer
            else:
                is_speaking = False
                s_queue.put_to_signal_q(signal)
                signal = b''

    stream.stop_stream()
    stream.close()
    audio.terminate()


def __recognition_process(
        s_queue: SharedQueue,
        state: __StateManager,) -> None:
    while state.is_recognizing:
        signal = s_queue.get_from_signal_q()
        recognized_text = __signal_to_text(signal)
        if recognized_text == FINISH_KEYWORD:
            stop()

        morphemes = __morpheme_analysis(recognized_text)
        lr_buffer = ""
        for m in morphemes:
            if m == "右" or m == "左":
                lr_buffer = m
                continue

            if lr_buffer != "" and (m == "肘" or m == "膝" or m == "また"):
                s_queue.put_to_morpheme_q(lr_buffer + m)
                lr_buffer = ""
            elif lr_buffer != "":
                s_queue.put_to_morpheme_q(lr_buffer)
                s_queue.put_to_morpheme_q(m)
                lr_buffer = ""
            else:
                s_queue.put_to_morpheme_q(m)

        for rt in recognized_text:
            s_queue.put_to_speech_q(rt)


def __signal_to_text(
        signal: bytes,) -> str:
    loss_bytes = len(signal) % (SAMPLE_RATE * 2)
    if loss_bytes != 0:
        signal += b'\x00' * (SAMPLE_RATE * 2 - loss_bytes)

    recognizer = sr.Recognizer()
    recognized_text = ""
    try:
        audio_data = sr.AudioData(signal, SAMPLE_RATE, 2)
        recognized_text = recognizer.recognize_google(
            audio_data,
            language="ja-JP")
    except sr.UnknownValueError:
        pass
    except sr.RequestError:
        pass
    finally:
        del recognizer
        return recognized_text


def __morpheme_analysis(
        text: str,) -> list:
    wakati = Tagger("-Owakati")
    morphemes = wakati.parse(text).split()
    del wakati
    return morphemes


def __printing_process(
        s_queue: SharedQueue,
        state: __StateManager,
        cf: ContentField,) -> None:
    while state.is_printing:
        speech_c = s_queue.get_from_speech_q()
        cf.update_value(speech_c)
        s_queue.done_speech_q()
        time.sleep(PRINT_INTERVAL)


def __analyzing_process(
        s_queue: SharedQueue,
        commander: Commander,
        state: __StateManager,) -> None:
    while state.is_analyzing:
        morpheme = s_queue.get_from_morpheme_q()
        
        if morpheme in ics_dict and commander.fetch_option() == 1:
            commander.add_ics(ics_dict[morpheme])
        elif morpheme in option_dict and commander.fetch_ics_list() != []:
            commander.set_option(option_dict[morpheme])
        elif morpheme in direction_dict and commander.fetch_ics_list() != []:
            commander.set_direction(direction_dict[morpheme])
            commander.send_command()
            commander.reset_command_buffer()
        elif morpheme == "リセット":
            commander.reset_command_buffer()
            commander.reset_position()


if __name__ == "__main__":
    init()
    # run()
