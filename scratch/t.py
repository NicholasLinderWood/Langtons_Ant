import argparse
import curses
import random
import shutil
import time
from collections import defaultdict
from collections.abc import Sequence
from typing import Generator

ROWS, COLUMNS = shutil.get_terminal_size()


def get_direction(direction: str) -> complex:
    if direction == 'up':
        return complex(0, 1)
    if direction == 'down':
        return complex(0, -1)
    if direction == 'left':
        return complex(-1, 0)
    if direction == 'right':
        return complex(1, 0)

    raise ValueError(
        f'got {direction=}, expected up, down, left, or right',
    )


def update_location(
    location: complex,
    direction: complex,
) -> complex:

    location += direction

    if location.real >= ROWS:
        real = 0
    elif location.real < 0:
        real = ROWS - 1
    else:
        real = location.real

    if location.imag >= COLUMNS:
        imag = 0
    elif location.imag < 0:
        imag = COLUMNS - 1
    else:
        imag = location.imag

    if (imag == COLUMNS - 1) and (real == ROWS - 1):
        imag = 0

    return complex(real, imag)


def ant(
    x: int,
    y: int,
    direction='up'
) -> Generator[complex, bool, None]:
    location = complex(x, y)
    direction = get_direction(direction)
    yield location
    while True:
        state = yield location
        if state:
            direction *= complex(0, 1)
        else:
            direction *= complex(0, -1)
        location = update_location(location, direction)


def grid() -> Generator[defaultdict[complex, bool], complex, None]:
    d: defaultdict[complex, bool] = defaultdict(bool)
    yield d
    while True:
        location = yield d
        d[location] = not d[location]


def langtons_ant(
    ants: list[Generator[complex, bool, None]],
) -> Generator[tuple[float, float, bool]]:
    locations = {a: next(a) for a in ants}
    g = grid()
    grid_state = next(g)
    while True:
        for a in locations:
            loc = a.send(grid_state[locations[a]])
            locations[a] = loc
            grid_state = g.send(loc)
            yield loc.real, loc.imag, grid_state[loc]


def c_main(
    stdscr: curses.window,
    n: int,
) -> int:
    curses.start_color()
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    if n == 1:
        la = langtons_ant([ant(ROWS // 2, COLUMNS // 2, 'up')])
    else:
        la = langtons_ant([
            ant(
                random.randrange(0, ROWS),
                random.randrange(0, COLUMNS),
                random.choice(['up', 'down', 'left', 'right']),
            )
            for _ in range(n)
        ])

    while True:
        x, y, state = next(la)
        if state:
            color_number = 2
        else:
            color_number = 1
        stdscr.addch(int(y), int(x), ' ', curses.color_pair(color_number))
        stdscr.refresh()
        time.sleep(0.001)
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--n',
        type=int,
        default=1,
    )
    args = parser.parse_args()
    return curses.wrapper(c_main, args.n)


if __name__ == '__main__':
    raise SystemExit(main())
