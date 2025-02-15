from queue import Queue

import flet as ft

class ContentField(ft.TextField):
    """ContentField class

    Speech content is displayed in this field.
    """
    def __init__(self) -> None:
        super().__init__(
            multiline=True,
            read_only=True,)
        
        self.speech_q = Queue()

    def update_value(self, value: str) -> None:
        self.value += value
        self.update()