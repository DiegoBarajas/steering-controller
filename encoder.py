from machine import Pin
import time

class RotaryEncoder:
    def __init__(self, pin_a_number, pin_b_number):
        self.pin_a = Pin(pin_a_number, Pin.IN)
        self.pin_b = Pin(pin_b_number, Pin.IN)
        self.last_a = self.pin_a.value()
        self.position = 0
        self.degrees = 0

        self.pin_a.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self._rotation_callback)

    def _rotation_callback(self, pin):
        a_value = self.pin_a.value()
        b_value = self.pin_b.value()

        if self.last_a != a_value:
            if a_value != b_value:
                self.position += 1
            else:
                self.position -= 1

        self.degrees = self.position * 1.8
        self.last_a = a_value

    def get_degrees(self):
        return self.degrees
