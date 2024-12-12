from Bts7960 import Bts7960
from encoder import RotaryEncoder
from time import sleep, time
import math

class SteeringController:
    def __init__(self, encoder_pins, motor_pins, freq=1000):
        pin_a_number, pin_b_number = encoder_pins
        rpwm_pin, lpwm_pin, ren_pin, len_pin = motor_pins

        self.encoder = RotaryEncoder(pin_a_number, pin_b_number)
        self.motor = Bts7960(rpwm_pin, lpwm_pin, ren_pin, len_pin, freq)
        
    def move_degrees(self, move=0, tolerance=2):
        target = self.encoder.get_degrees() + move

        while abs(self.encoder.get_degrees() - target) > tolerance:
            degrees_to_target = abs(self.encoder.get_degrees() - target)
            positive = -1 if (target - self.encoder.get_degrees()) > 0 else 1

            if degrees_to_target-(tolerance*0.5) <= 0: break

            if degrees_to_target > 360:
                self.motor.start(100 * positive)
            elif degrees_to_target > 315:
                self.motor.start(90 * positive)
            elif degrees_to_target > 270:
                self.motor.start(80 * positive)
            elif degrees_to_target > 225:
                self.motor.start(70 * positive)
            elif degrees_to_target > 180:
                self.motor.start(60 * positive)
            elif degrees_to_target > 135:
                self.motor.start(50 * positive)
            elif degrees_to_target > 90:
                self.motor.start(45 * positive)
            elif degrees_to_target > 45:
                self.motor.start(30 * positive)
            elif degrees_to_target > 10:
                self.motor.start(20 * positive)
            else:
                self.motor.start(15 * positive)

            sleep(0.05)
            degrees_to_target = abs(self.encoder.get_degrees() - target)
        
        self.motor.stop()
        sleep(0.1)

    def sinusoidal_motion(self, amplitude=180, times=20):
        self.move_degrees(-self.encoder.get_degrees())
        cont = -1
        for _ in range(times):
            start_time = time()
            self.move_degrees(amplitude * cont)
            end_time = time()

            cont *= -1
            sleep(max(5 - (end_time - start_time), 0))
            
    def move_to_zero(self):
        self.move_degrees(-self.encoder.get_degrees(), 5)
        
        
    def follow(self):
        while True:
            self.move_to_zero()

