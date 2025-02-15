from queue import Queue

import flet as ft

import speechanalysis.analyzer as analyzer
from speechanalysis.content_field import ContentField


class RunButton(ft.Button):
    def __init__(self, cf: ContentField) -> None:
        super().__init__(
            text="Run",
            on_click=self.run,)
        self.cf = cf

    def run(self, e) -> None:
        self.cf.value = ""
        self.cf.update()
        analyzer.init()
        analyzer.run(self.cf)


class StopButton(ft.Button):
    def __init__(self, cf: ContentField) -> None:
        super().__init__(
            text="Stop",
            on_click=self.stop,)
        self.cf = cf

    def stop(self, e) -> None:
        analyzer.stop()


def main(page: ft.Page) -> None:
    cf = ContentField()
    rb = RunButton(cf)
    sb = StopButton(cf)

    # page.scroll = ft.ScrollMode.AUTO
    page.title = "KHRSpeechCommander"
    page.window.width = 300
    page.window.height = 400
    row = ft.Row(
        controls=[rb, sb])
    page.add(row, cf)
    page.update()


if __name__ == "__main__":
    ft.app(main)
