import time
import pigpio
import read_PWM

PWM_GPIO = 4
RUN_TIME = 1000.0
SAMPLE_TIME = 5.0

pi = pigpio.pi() # Grants access t Pi's GPIO

p = read_PWM.reader(pi, PWM_GPIO)

start = time.time()
while (time.time() - start) < RUN_TIME:

   time.sleep(SAMPLE_TIME)

   pp = p.pulse_period()
   pw = p.pulse_width()
   conc = 5000.0*(pw-2)/(pp-4)

   print("t={} pp={} pw={} c={}".format(time.time(), pp, pw, conc))

p.cancel()

pi.stop()

