from queue import Queue

import flet as ft

import speechanalysis.analyzer as analyzer
from speechanalysis.content_field import ContentField


class RunButton(ft.Button):
    """RunButton class

    This button runs speech analysis.
    """

    def __init__(self, cf: ContentField) -> None:
        """Initialize RunButton class

        Args:
            cf (ContentField): ContentField for updating value
        """
        super().__init__(
            text="Run",
            on_click=self.run,)
        self.cf = cf

    def run(self, e) -> None:
        """Run speech analysis"""
        self.cf.value = ""
        self.cf.update()
        analyzer.init()
        analyzer.run(self.cf)


class StopButton(ft.Button):
    """StopButton class

    This button stops speech analysis.
    """

    def __init__(self, cf: ContentField) -> None:
        """Initialize StopButton class

        Args:
            cf (ContentField): ContentField for updating value
        """
        super().__init__(
            text="Stop",
            on_click=self.stop,)
        self.cf = cf

    def stop(self, e) -> None:
        """Stop speech analysis"""
        analyzer.stop()


def main(page: ft.Page) -> None:
    """Main function"""
    cf = ContentField()
    rb = RunButton(cf)
    sb = StopButton(cf)

    page.scroll = ft.ScrollMode.AUTO
    page.title = "KHRSpeechCommander"
    page.window.width = 300
    page.window.height = 400
    row = ft.Row(
        controls=[rb, sb])
    page.add(row, cf)
    page.update()


if __name__ == "__main__":
    ft.app(main)
