#!/usr/bin/env python

# read_PWM.py
# 2015-12-08
# Public Domain

import time
import pigpio # http://abyz.co.uk/rpi/pigpio/python.html

class reader:
   """
   A class to read PWM pulses and calculate their frequency
   and duty cycle.  The frequency is how often the pulse
   happens per second.  The duty cycle is the percentage of
   pulse high time per cycle.

   Class "reader" has no common attributes.  Only instant attributes
   as described below (use of self is important).
   """

   def __init__(self, pi, gpio):
      """
      Instantiate with the Pi and gpio of the PWM signal
      to monitor.
      """
      self.pi = pi
      self.gpio = gpio

      self._high_tick = None
      self._period = None
      self._high = None

      pi.set_mode(gpio, pigpio.INPUT) # Sets the mode of gpio pin

      """
Calls a user supplied function (a callback) whenever the specified GPIO edge is detected. 
callback(user_gpio, edge, func)
user_gpio = 0-31
edge = EITHER_EDGE, RISING_EDGE (default), or FALLING_EDGE.
func = user supplied callback function. _cbf here.
      """

      self._cb = pi.callback(gpio, pigpio.EITHER_EDGE, self._cbf)

      """
The user supplied callback receives three parameters: 
the GPIO, the level, and the tick. 

Parameter   Value    Meaning

GPIO        0-31     The GPIO which has changed state

level       0-2      0 = change to low (a falling edge)
                     1 = change to high (a rising edge)
                     2 = no level change (a watchdog timeout)

tick        32 bit   The number of microseconds since boot
                     WARNING: this wraps around from
                     4294967295 to 0 roughly every 72 minutes
      """

   def _cbf(self, gpio, level, tick):

      if level == 1: # Change to high

         if self._high_tick is not None:

            """
pigpio.tickDiff(t1,t2) returns the microsesecond difference between two ticks.
Automatically takes care of the tick reset after roughly every 72 mins.
            """
            t = pigpio.tickDiff(self._high_tick, tick)
            self._period = t

         self._high_tick = tick

      elif level == 0: # Change to low

         if self._high_tick is not None:
            t = pigpio.tickDiff(self._high_tick, tick)
            self._high = t

   def frequency(self):
      """
      Returns the PWM frequency.
      """
      if self._period is not None:
         return 1000000.0 / self._period # Number of periods/second
      else:
         return 0.0

   def pulse_period(self):
      """
      Returns the PWM period
      """ 
      if self._period is not None:
         return self._period
      else:
         return 0.0

   def pulse_width(self):
      """
      Returns the PWM pulse width in microseconds.
      """
      if self._high is not None:
         return self._high
      else:
         return 0.0

   def duty_cycle(self):
      """
      Returns the PWM duty cycle percentage.
      """
      if self._high is not None:
         return 100.0 * self._high / self._period
      else:
         return 0.0

   def cancel(self):
      """
      Cancels the reader and releases resources.
      """
      self._cb.cancel()

if __name__ == "__main__":

   import time
   import pigpio
   import read_PWM

   PWM_GPIO = 4
   RUN_TIME = 1000.0
   SAMPLE_TIME = 2.0

   pi = pigpio.pi() # Grants access t Pi's GPIO

   p = read_PWM.reader(pi, PWM_GPIO)

   start = time.time()

   while (time.time() - start) < RUN_TIME:

      time.sleep(SAMPLE_TIME)

      pp = p.pulse_period()
      pw = p.pulse_width()
      conc = 5000.0*(pw-2)/(pp-4)
     
      print("t={} pp={} pw={} c={:.1f}".format(time.time(), pp, pw, conc))

   p.cancel()

   pi.stop()

