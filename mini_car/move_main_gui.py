#!/usr/bin/python
'''
impement gui with Tkinter. Try this.
try to implement PID control in this version.


'''
import RPi.GPIO as GPIO
import time
import car_drive
from pid_44 import PID_44, PID_1
import log_car
import Tkinter

#++HARDWARE SETTING+++++++++++++++++++++++++++++++++++
RIGHT_WHEEL_ENCODER     = 38
LEFT_WHEEL_ENCODER      = 40

#++SETTING PROCESS STEP++++++++++++++++++++++++++++++++++++++++++++
EXEC_TIME               = 25
TIC_SETTING             = 1  #if normal, (EXEC_TIME * TIC_SETTING) is all time
TIC_GUARDBAND           = 0.05
BOUNCE_TIME             = 30
VERBOSE                 = True   #True to enable, False to disable timing log

#++SETTING-PID++++++++++++++++++++++++++++++++++++++++++++
TAR_EN_COUNT1     = 15
IN_POWER1         = 800

TAR_EN_COUNT2     = 15
IN_POWER2         = 2500

M_DEVIATION       = 1800
M_DEVIATION_DELTA = 800

#++INITIALIZATION++++++++++++++++++++++++++++++++++++++++++++
mission_status=0
en_counter_r=0
en_counter_l=0

#timing_tic=0  #global timing to calulate delta time in log_car.timing_log function

def call_back_encoder_right(channel):
    global en_counter_r
    en_counter_r+=1

def call_back_encoder_left(channel):
    global en_counter_l
    en_counter_l+=1

GPIO.setmode(GPIO.BOARD)
GPIO.setup(RIGHT_WHEEL_ENCODER, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LEFT_WHEEL_ENCODER, GPIO.IN, pull_up_down=GPIO.PUD_UP)


GPIO.add_event_detect(RIGHT_WHEEL_ENCODER, GPIO.FALLING,\
                     callback=call_back_encoder_right, bouncetime=BOUNCE_TIME)
GPIO.add_event_detect(LEFT_WHEEL_ENCODER, GPIO.FALLING,\
                     callback=call_back_encoder_left, bouncetime=BOUNCE_TIME)

car= car_drive.car_simple_drive(debug=False)

pid_right=PID_1(P=40.0, I=20.0, D=5.0, Derivator=0, Integrator=0, \
  Integrator_max=M_DEVIATION, \
  Integrator_min=-1*M_DEVIATION, set_point= TAR_EN_COUNT1)


pid_delta=PID_1(P=40.0, I=20.0, D=5.0, Derivator=0, Integrator=0, \
  Integrator_max=M_DEVIATION_DELTA, \
  Integrator_min=-1*M_DEVIATION_DELTA, set_point= 0)

log_car.mission_log(0, "****** Mission starts normally ******")

if VERBOSE:
  log_car.timing_log(0 , str(en_counter_l)+" ,"+str(en_counter_r))

time_stamp_start=time.time()


print "start to monitoring"

car.move(+1, IN_POWER1, 0)

power_deviation = 0
power_deviation_delta = 0
pre_en_counter_r = 0
#++START OF INFINITE LOOP++++++++++++++++++++++++++++++++++++++++++++

for loop_i in range(EXEC_TIME):
  #test
  #++++take a tic here++++++
  a = time.time()

  #++++calculation of pid for right wheel ++++++
  power_deviation, p, i, d, error = pid_right.update(en_counter_r-pre_en_counter_r)
  pre_en_counter_r=en_counter_r
  print "in main loop: ", power_deviation, p,i,d, error
  #limit range of power_deviation
  if power_deviation > 0:
    power_deviation=min(power_deviation, M_DEVIATION)
  else:
    power_deviation=max(power_deviation, -1*M_DEVIATION)
  
  #++++calculation of pid for delta change ++++++
  power_deviation_delta, p_d, i_d, d_d, error_d = pid_delta.update(en_counter_l-en_counter_r)
  print "in main loop: ", power_deviation_delta, p_d,i_d,d_d, error_d

  if power_deviation_delta > 0:
    power_deviation_delta=min(power_deviation_delta, M_DEVIATION_DELTA)
  else:
    power_deviation_delta=max(power_deviation_delta, -1*M_DEVIATION_DELTA)
  
  #++++update the power for each wheel ++++++
  power_right= IN_POWER1 + power_deviation
  power_left= power_right + power_deviation_delta 

  if VERBOSE:
    log_car.timing_log(loop_i, " ," + str(en_counter_r)+" ,"+str(en_counter_l)\
      + " ," + str(power_right)+ " ,"+str(power_left)\
      + " ," + str(power_deviation)+ " ," + str(power_deviation_delta))

  car.move(1, power_right, power_left)
  #
  #++Check if loop time is too long, give warning and log it.
  if (time.time()-a) > (TIC_SETTING-TIC_GUARDBAND):
    log_car.mission_log(loop_i, "Warning: Loop time exceed TIC_SETTING: "+ str(TIC_SETTING))
    mission_status = 1
    break

  #++++++++++wait until next tic pass
  time.sleep(TIC_SETTING+a-time.time())

car.stop_wait()
time.sleep(5)
'''
power_deviation = 0
power_deviation_delta = 0
pre_en_counter_r = 0
'''

#++START OF INFINITE LOOP++++++++++++++++++++++++++++++++++++++++++++

for loop_i in range(EXEC_TIME):
  #test
  #++++take a tic here++++++
  a = time.time()

  #++++calculation of pid for right wheel ++++++
  power_deviation, p, i, d, error = pid_right.update(en_counter_r-pre_en_counter_r)
  pre_en_counter_r=en_counter_r
  print "in main loop: ", power_deviation, p,i,d, error
  #limit range of power_deviation
  if power_deviation > 0:
    power_deviation=min(power_deviation, M_DEVIATION)
  else:
    power_deviation=max(power_deviation, -1*M_DEVIATION)
  
  #++++calculation of pid for delta change ++++++
  power_deviation_delta, p_d, i_d, d_d, error_d = pid_delta.update(en_counter_l-en_counter_r)
  print "in main loop: ", power_deviation_delta, p_d,i_d,d_d, error_d

  if power_deviation_delta > 0:
    power_deviation_delta=min(power_deviation_delta, M_DEVIATION_DELTA)
  else:
    power_deviation_delta=max(power_deviation_delta, -1*M_DEVIATION_DELTA)
  
  #++++update the power for each wheel ++++++
  power_right= IN_POWER1 + power_deviation
  power_left= power_right + power_deviation_delta 

  if VERBOSE:
    log_car.timing_log(loop_i, " ," + str(en_counter_r)+" ,"+str(en_counter_l)\
      + " ," + str(power_right)+ " ,"+str(power_left)\
      + " ," + str(power_deviation)+ " ," + str(power_deviation_delta))

  car.move(-1, power_right, power_left)
  #
  #++Check if loop time is too long, give warning and log it.
  if (time.time()-a) > (TIC_SETTING-TIC_GUARDBAND):
    log_car.mission_log(loop_i, "Warning: Loop time exceed TIC_SETTING: "+ str(TIC_SETTING))
    mission_status = 1
    break

  #++++++++++wait until next tic pass
  time.sleep(TIC_SETTING+a-time.time())
#++END OF INFINITE LOOP++++++++++++++++++++++++++++++++++++++++++++

car.stop_wait()
time.sleep(3)
car.turn_90(0)
time.sleep(3)
car.turn_90(0)
time.sleep(3)

car.turn_90(0)
time.sleep(3)
car.turn_90(0)
time.sleep(3)

#++MISSION REPORT++++++++++++++++++++++++++++++++++++++++++++ 
if mission_status== 0:
  log_car.mission_log(i, "Mission ends normally" + " execution time: " + \
      str(time.time()-time_stamp_start))
  print "end normally"
else :
  mission_log(i, "Mission ends abnormally "+ " execution time: " + \
      str(time.time()-time_stamp_start))
  print "end abnormally"


GPIO.cleanup()
