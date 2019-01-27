from random import randint
from asciimatics.screen import Screen
import time

def demo(screen):

    count = 0
    while True:
        time.sleep(0.2)
        count+=1
        screen.print_at('Hello world! {}'.format(count),
                        0, 0)
        ev = screen.get_key()
        if ev in (ord('Q'), ord('q')):
            return
        screen.refresh()

Screen.wrapper(demo)
