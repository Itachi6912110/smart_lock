import sys

import RPi.GPIO as gpio
from modules.controller import Controller

PINS = []
controller = Controller(PINS) # motor pins (a list)

def slipper_1_out():
  controller.slipper_move(0, "forward")

def slipper_2_out():
  controller.slipper_move(1, "forward")

def slipper_3_out():
  controller.slipper_move(2, "forward")

def slipper_1_in():
  controller.slipper_move(0, "backward")

def slipper_2_in():
  controller.slipper_move(1, "backward")

def slipper_3_in():
  controller.slipper_move(2, "backward")

if __name__ == '__main__':
  gpio.setmode(gpio.BCM)
  try:
    slipper_1_out()
    print ("slipper 1 is coming...")
  except KeyboardInterrupt:
    print('Interrupt, Exiting...')
  finally:
    print('Exiting...')
    controller.stop()
    gpio.cleanup()
    exit(-1)

