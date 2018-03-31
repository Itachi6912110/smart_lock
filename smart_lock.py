import subprocess as sb

from RPi import GPIO as gpio
from time import sleep

if gpio.getmode() != gpio.BCM:
    gpio.setmode(gpio.BCM)

in_human_sense_pin = 3
out_human_sense_pin = 3

#human sensor set up
gpio.setup(in_human_sense_pin, gpio.IN)
gpio.setup(out_human_sense_pin, gpio.IN)

while True:
	if gpio.input(out_human_sense_pin):
		sb.run(["python3", "speech.py"])
		sb.run(["python3", "face_recog.py"])

	if gpio.input(in_human_sense_pin):
		sb.run(["python3", "goout.py"])

