import datetime
from textual import work
from textual.app import App, ComposeResult
from textual.widgets import Static
from asyncio import sleep as asyncio_sleep

# https://symbl.cc/en/unicode-table/#block-elements


class Clock(App):
    BINDINGS = [("ctrl+q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Static("", id="main")

    def on_mount(self) -> None:
        static_zone = self.query_one("#main", Static)
        self.update(static_zone)

    @work
    async def update(self, static_zone: Static) -> None:
        def build_lines(layout, value):
            lines = []
            for y in range(len(layout)):
                line = [
                    ("█" if (value > layout[y][x]) else "▁")
                    for x in range(len(layout[0]))
                ]
                lines.append(line)
            return lines

        def hours(h):
            hours_layout = [
                [1, 2, 13, 14],
                [3, 4, 15, 16],
                [5, 6, 17, 18],
                [7, 8, 19, 20],
                [9, 10, 21, 22],
                [11, 12, 23, 24],
            ]
            return build_lines(hours_layout, h)

        def minutes(m):
            minutes_layout = [
                [1, 2, 3, 4, 5, 16, 17, 18, 19, 20],
                [6, 7, 8, 9, 10, 21, 22, 23, 24, 25],
                [11, 12, 13, 14, 15, 26, 27, 28, 29, 30],
                [31, 32, 33, 34, 35, 46, 47, 48, 49, 50],
                [36, 37, 38, 39, 40, 51, 52, 53, 54, 55],
                [41, 42, 43, 44, 45, 56, 57, 58, 59, 60],
            ]
            return build_lines(minutes_layout, m)

        def seconds(s):
            seconds_layout = [
                [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                [11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
                [21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
                [31, 32, 33, 34, 35, 36, 37, 38, 39, 40],
                [41, 42, 43, 44, 45, 46, 47, 48, 49, 50],
                [51, 52, 53, 54, 55, 56, 57, 58, 59, 60],
            ]
            return build_lines(seconds_layout, s)

        def collate(a, b, sep=" "):
            return [a[y] + [sep] + b[y] for y in range(len(a))]

        def colapse(m) -> str:
            lines = ""
            for y in range(len(m)):
                lines += "".join([x for x in m[y]]) + "\n"
            return lines

        while True:
            now = datetime.datetime.now()
            mh = hours(now.hour)
            mm = minutes(now.minute)
            ms = seconds(now.second)
            collated = collate(collate(mh, mm), ms)
            static_zone.update(colapse(collated))
            await asyncio_sleep(1)


def main():
    app = Clock()
    app.run()


if __name__ == "__main__":
    main()
