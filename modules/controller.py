from RPi import GPIO as gpio
import time
from time import sleep

RUN_TIME = 3  #run time for slipper car

class Controller(object):
  def __init__(self, motor_pins, servo_pin, sonar_pins):
    if gpio.getmode() != gpio.BCM:
      gpio.setmode(gpio.BCM)
    #setup motors
    self.motors = motor_pins # motors is a list contains motor pins
    for m in self.motors:
      gpio.setup(m, gpio.OUT)
    
    #setup servo 
    gpio.setup(servo_pin, gpio.OUT)
    self.servo = gpio.PWM(servo_pin, 50)
    self.middle_val = 8.3
    self.left_val = self.middle_val - 1.6
    self.right_val = self.middle_val + 1.6

    #setup sonar
    gpio.setup(sonar_pins[0], gpio.OUT) #sonar_pins = [trigger_pin, echo_pin]
    gpio.setup(sonar_pins[1], gpio.IN)
    self.trigger_pin = sonar_pins[0]
    self.echo_pin = sonar_pins[1]

  #define motor funcs
  def slipper_move(self, num, mode=0): # you cannot call twice
    if mode == "backward":
      num = (-1) * (num + 1)
    gpio.output(self.motors[num], 1)
    sleep(RUN_TIME)

  def stop(self):
    for m in self.motors:
      gpio.output(m, 0)

  def cleanup(self):
	  gpio.cleanup()

  #def servo funcs
  def lock(self):
    self.servo.start(self.middle_val)

  def open(self):
    self.servo.start(self.left_val)
    sleep(3)

  #def sonar funcs
  def send_trigger_pulse(self):
    gpio.output(self.trigger_pin, True)
    time.sleep(0.001)
    gpio.output(self.trigger_pin, False)

  def wait_for_echo(self, value, timeout):
    count = timeout
    while gpio.input(self.echo_pin) != value and count > 0:
        count = count - 1

  def get_distance(self):
    self.send_trigger_pulse()
    self.wait_for_echo(True, 5000)
    start = time.time()
    self.wait_for_echo(False, 5000)
    finish = time.time()
    pulse_len = finish - start
    distance_cm = pulse_len * 340 *100 /2
    return distance_cm
