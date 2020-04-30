from IPython import embed
from ipydex import dirsearch

import pygame
import xbox360_controller as x
import time

pygame.init()
c = x.Controller()

done = False
noevents = 0
while not done:
    # event handling (not doing this hangs everything)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done=True

    # joystick stuff
    if noevents >= 10**5:
        print(f"Reset noevents: {noevents}")
        noevents = 0
        c.initjoystick()
        # embed()

    if c.joystick is None:
        noevents += 1
        continue

    pressed = c.get_buttons()

    abtn = pressed[x.A]
    bbtn = pressed[x.B]
    xbtn = pressed[x.X]
    ybtn = pressed[x.Y]
    back = pressed[x.BACK]
    start = pressed[x.START]
    guide = pressed[x.GUIDE]
    lt_bump = pressed[x.LEFT_BUMP]
    rt_bump = pressed[x.RIGHT_BUMP]
    lt_stick_btn = pressed[x.LEFT_STICK_BTN]
    rt_stick_btn = pressed[x.RIGHT_STICK_BTN]

    lt_x, lt_y = c.get_left_stick()
    rt_x, rt_y = c.get_right_stick()

    triggers = c.get_triggers()

    pad_up, pad_right, pad_down, pad_left = c.get_pad()

    if abtn == 1:
        print(f"a: {abtn}")
    if guide == 1:
        print(f"guide: {guide}")
    if not (abtn or guide):
        noevents += 1
    else:
        noevents = 0

    # time.sleep(0.001)

# close window on quit
pygame.quit()
