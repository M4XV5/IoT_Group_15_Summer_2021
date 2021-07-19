#!/usr/bin/python3.7
import RPi.GPIO as GPIO

# set gpio mode to board
GPIO.setmode(GPIO.BOARD)

# fan
GPIO.setup(16, GPIO.OUT)
GPIO.output(16, GPIO.LOW)

# buttons
GPIO.setup(35, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(38, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(40, GPIO.OUT)
GPIO.output(40, GPIO.LOW)

# led door
GPIO.setup(36, GPIO.OUT)
GPIO.output(36, GPIO.LOW)


#led emer
GPIO.setup(33, GPIO.OUT)
GPIO.output(33, GPIO.LOW)

# led room
GPIO.setup(37, GPIO.OUT)
GPIO.output(37, GPIO.LOW)

# cleanup resets all GPIO pins   
GPIO.cleanup()
print("All GPIO Pins cleaned up!")