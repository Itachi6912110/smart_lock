import sys

import RPi.GPIO as gpio
from modules.controller import Controller

MOTOR_PINS = [13, 19, 26, 21, 20, 16]
SERVO_PIN = 18
SONAR_PINS = [23, 24]
controller = Controller(MOTOR_PINS, SERVO_PIN, SONAR_PINS) # motor pins (a list)

#parameters
CLOSE_DIST = 3  #distance of when to lock the door

#def for slipper cars
def slipper_1_out():
  controller.slipper_move(0, "forward")
  controller.stop()

def slipper_2_out():
  controller.slipper_move(1, "forward")
  controller.stop()

def slipper_3_out():
  controller.slipper_move(2, "forward")
  controller.stop()

def slipper_1_in():
  controller.slipper_move(0, "backward")
  controller.stop()

def slipper_2_in():
  controller.slipper_move(1, "backward")
  controller.stop()

def slipper_3_in():
  controller.slipper_move(2, "backward")
  controller.stop()

#def for lock
def open_door():    #open door and lock back when the door is close enough
  print("openning door ...")
  controller.open()
  while True :
    print(controller.get_distance())
    if controller.get_distance() < CLOSE_DIST:
      print("locking door ...")
      controller.lock()
      break

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

