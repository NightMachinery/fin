from IPython import embed
from ipydex import dirsearch

import pygame
import xbox360_controller as x
import time, os
from collections import deque
from dataclasses import dataclass
import typing
import datetime

###
PAD_BASE = 20
LEFT_STICK_BASE = 30
RIGHT_STICK_BASE = 40
ROTATIONS_BASE = 50
TRIGGER_BASE = 60
###
@dataclass
class State:
    state: typing.Any
    
    handled: bool
    finalized: bool
    date: datetime.datetime

    def __init__(self, state, handled=False, finalized=True):
        self.state = state
        self.handled = handled
        self.finalized = finalized
        self.date = datetime.datetime.now()
###
pygame.init()
dbg = os.environ.get('DEBUGME', '')
c = x.Controller(dead_zone=0.2)

g = [deque(maxlen=10) for i in range(100)]  # global state of all keys


def updateG(id, state, force=False):
    d = g[id]
    needsUpdate = True
    if not force and d:
        # d not empty
        last = d[-1]
        if last.state == state:
            needsUpdate = False
    if force or needsUpdate:
        d.append(State(state))
        if True or dbg:
            print(f"updated id: {id} state: {state}")
    return needsUpdate

def updateBtn(id, pressed):
    return updateG(id, pressed[id])

def updateDir(id_base, c_dir):
    for dir in x.SDir:
        if dir == x.SDir.NEUTRAL:
            continue
        if updateG(id_base + dir.value, c_dir == dir) and dbg:
            # print(f"s1 angle: {x.stick2angle(lt_x,lt_y)}")
            print(f"{id_base} c_dir: {c_dir}")

def updateRotation(id, ids, allow_dups=True):
    d = g[id]
    def addNew():
        if dbg:
            print(f"Adding new rotation deque for {id}")
        d.append(State(deque(maxlen=10), finalized=False))
    needsNew = False
    if not d:
        # d empty
        needsNew = True
    elif d[-1].finalized:
        needsNew = True
    if needsNew:
        addNew()
    lrot_s = d[-1]
    lrot = lrot_s.state
    neutral = True
    for key_id in ids:
        key = g[key_id][-1].state
        if key:
            neutral = False
            if not lrot or (allow_dups and lrot[-1] != key_id) or (not allow_dups and not key_id in lrot):
                lrot.append(key_id)
    if len(lrot) > 0 and neutral:
        lrot_s.finalized = True
        addNew()
        if dbg:
            # print(f"\nrotations {id}: {d}\n")
            print(f"last rotation {id}: {lrot_s.state}")
        return True
    return False


done = False
noevents = 0
while not done:
    # event handling (not doing this hangs everything)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # joystick stuff
    if noevents >= 10 ** 5:
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
    lt_dir = x.stick2dir(lt_x, lt_y)
    rt_x, rt_y = c.get_right_stick()
    rt_dir = x.stick2dir(rt_x, rt_y)

    triggers = c.get_triggers()

    pad_up, pad_right, pad_down, pad_left = map(bool, c.get_pad())

    noevents = 0

    updateDir(LEFT_STICK_BASE, lt_dir)
    updateDir(RIGHT_STICK_BASE, rt_dir)
    updateG(PAD_BASE + 1, pad_right and not (pad_up or pad_down))
    updateG(PAD_BASE + 2, pad_right and pad_up)
    updateG(PAD_BASE + 3, pad_up and not (pad_left or pad_right))
    updateG(PAD_BASE + 4, pad_left and pad_up)
    updateG(PAD_BASE + 5, pad_left and not (pad_up or pad_down))
    updateG(PAD_BASE + 6, pad_left and pad_down)
    updateG(PAD_BASE + 7, pad_down and not (pad_left or pad_right))
    updateG(PAD_BASE + 8, pad_right and pad_down)

    if updateG(TRIGGER_BASE, triggers > 0.2) and dbg:
        print(f"triggers: {triggers}")
    updateG(TRIGGER_BASE + 1, triggers >= 0.999)
    updateRotation(TRIGGER_BASE + 2, [TRIGGER_BASE + i for i in range(0,2)], allow_dups = False)

    updateBtn(x.RIGHT_BUMP, pressed)
    updateBtn(x.LEFT_BUMP, pressed)
    updateBtn(x.RIGHT_STICK_BTN, pressed)
    updateBtn(x.LEFT_STICK_BTN, pressed)
    updateBtn(x.B, pressed)
    updateBtn(x.Y, pressed)
    updateBtn(x.X, pressed)
    updateBtn(x.A, pressed)
    updateBtn(x.START, pressed)
    updateBtn(x.GUIDE, pressed)
    updateBtn(x.BACK, pressed)
    # updateBtn(x., pressed)

    
    updateRotation(ROTATIONS_BASE, [LEFT_STICK_BASE + i for i in range(1,9)])
    updateRotation(ROTATIONS_BASE + 1, [RIGHT_STICK_BASE + i for i in range(1,9)])
    updateRotation(ROTATIONS_BASE + 2, [PAD_BASE + i for i in range(1,9)])
    # print(f"L RIGHT: {g[20 + x.SDir.RIGHT.value]}")
    # print(f"rt_bump: {g[x.RIGHT_BUMP]}")

    # if abtn == 1:
    #     print(f"a: {abtn}")
    # if guide == 1:
    #     print(f"guide: {guide}")
    # if not (abtn or guide):
    #     noevents += 1
    # else:
    #     noevents = 0

    # time.sleep(0.001)

# close window on quit
pygame.quit()
