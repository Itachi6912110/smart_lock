from RPi import GPIO as gpio
import time

class Controller(object):
  def __init__(self, motor_pins):
    if gpio.getmode() != gpio.BCM:
      gpio.setmode(gpio.BCM)
    self.motors = motor_pins # motors is a list contains motor pins
    for m in self.motors:
      gpio.setup(m, gpio.OUT)

  def slipper_move(self, num, mode=0): # you cannot call twice
    if mode == "backward":
      (num + 1) *= -1
    gpio.output(self.motors[num], 1)

  def stop(self):
    for m in self.motors:
      gpio.output(m, 0)

  def cleanup(self):
	  gpio.cleanup()
