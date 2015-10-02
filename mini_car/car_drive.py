#!/usr/bin/python
from Adafruit_PWM_Servo_Driver import PWM
import time
'''
LEARN ABSTRACTION WITH THIS.
move portion of car, how to move car.
car_driver.py
This provide some useful class to be used while driving wheels.
gordon.yiu@gmail.com
'''
#++wheel_drive++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class wheel_drive:
	'''
	control of single wheel

	'''
	#pwm channel no. to control motor, hardware wiring
	__RIGHT_FORWARD_PWM_CH			= 0 	#pwm channel 0 and 1 drive right motor
	__RIGHT_BACKWARD_PWM_CH			= 1
	__LEFT_FORWARD_PWM_CH			= 2		#pwm channel 2 and 3 drive right motor
	__LEFT_BACKWARD_PWM_CH			= 3

	#setting
	__I2C_ADDRESS_PWM_DRIVER		= 0X40 	#i2c default address for PCA9685
	__MOTOR_DRIVE_PWM_FREQUENCY		= 200 	#Hz
	__TIME_DELAY_GO_OTHER_DIR		= 0.15  	#in s, wait then wheel turn other direction

	motor_control_pwm=PWM(__I2C_ADDRESS_PWM_DRIVER,debug=False)

	@classmethod
	def set_motor_control_pwm_frequency(cls, debug=False):
		cls.motor_control_pwm.setPWMFreq(cls.__MOTOR_DRIVE_PWM_FREQUENCY)
		if debug: print "set pwm frequency to "+ str(cls.__MOTOR_DRIVE_PWM_FREQUENCY) + " Hz"


	def __init__(self, right_or_left=0,debug=False):

		self.side=right_or_left  	# 0 for right wheel, 1 for left wheel
		self.direction=0  			# 0 for forward
		self.debug=debug			# True to turn on verbose debug

		if self.side:
			self.pwm_f=self.__RIGHT_FORWARD_PWM_CH		# pwm channel for driving motor forward
			self.pwm_b=self.__RIGHT_BACKWARD_PWM_CH	
		else:
			self.pwm_f=self.__LEFT_FORWARD_PWM_CH
			self.pwm_b=self.__LEFT_BACKWARD_PWM_CH
		
		self.stop()

		if self.debug: print "initialize wheel side: "+ str(self.side)

	def set_dir_power(self,direction= 0,pwm= 0):
		'''
		for single wheel control
		set power in PWM range from 0 to 4095
		set dir in 0 -forward or 1-backward
		basically change two pwm channels for a single motor to drive wheel
		set one pwm channel to 0 and other pwm to drive.
		'''
		#go the other dir, wheel_stop and then go
		if self.direction!=direction:
			if self.debug: print "Turn to other direction"
			self.stop()
			time.sleep(self.__TIME_DELAY_GO_OTHER_DIR)
			self.direction=direction

		#go same dir, just go
		else:
			if self.debug: print "Same direction"

		if self.direction:
			self.motor_control_pwm.setPWM(self.pwm_b,0, pwm)
		else:
			self.motor_control_pwm.setPWM(self.pwm_f,0, pwm)

		if self.debug: 
			print "set to wheel: "+str(self.side)+ \
			", dir: " +str(self.direction)+ " pwm ouput: " + str(pwm)

	def stop(self):
		self.motor_control_pwm.setPWM(self.pwm_f,0,0)
		self.motor_control_pwm.setPWM(self.pwm_b,0,0)

	def glide():
		pass
#++car_drive++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class car_simple_drive():
	'''
	control of whole car which consists of two wheels
	using simple and direct driving method, a lot of manual calibrations are needed.

	'''
	# tons of calibration constant
	# Car statud
	__CAR_STOP				= 0
	__CAR_FORWARD			= 1
	__CAR_BACKWARD			= -1
	__CAR_TURN				= 2
	__CAR_UB				= 3

	# turn calibration constant, in time, right power, left power order
	__TURN_90							= (1, 1500,1550)
	__TURN_180							= (1.24, 1730, 1750)
	# move forward calibration constant, in (low speed right power, left power),(med), (high)) order
	__MOVE_FORWARD						= ((2000,1850),(3000,3000),(3072,3072))
	__MOVE_BACKWARD						= ((2000,1850),(2048,2048),(3072,3072))

	#
	def __init__(self, debug=False):
		self.debug = debug		#True to turn on verbose
		#call to set frequency before instance, so class method is needed.
		wheel_drive.set_motor_control_pwm_frequency(debug=self.debug)
		#instance right wheel and left wheel
		self.right_wheel=wheel_drive(1, debug=self.debug)
		self.left_wheel=wheel_drive(0, debug=self.debug)
		self.stop_wait()

	def move(self, *args): 		# in (self, dir, right_power, left_power) order
		if len(args)==3 and (args[0] in [self.__CAR_BACKWARD,self.__CAR_FORWARD]):
			if self.car_move_status not in [self.__CAR_STOP, args[0]]: self.stop_wait()
			self.right_wheel.set_dir_power((0,1)[args[0] != self.__CAR_FORWARD], int(args[1]))
			self.left_wheel.set_dir_power((0,1)[args[0] != self.__CAR_FORWARD], int(args[2]))
			self.car_move_status = args[0]
		return

	def move_forward(self, speed, move_time=0):		#speed =0 for low and 1 med, 2 high
		if self.car_move_status not in [self.__CAR_STOP, self.__CAR_FORWARD]: self.stop_wait()
		self.right_wheel.set_dir_power(0, self.__MOVE_FORWARD[speed][0])
		self.left_wheel.set_dir_power(0, self.__MOVE_FORWARD[speed][1])
		self.car_move_status = self.__CAR_FORWARD
		if move_time!=0:
			time.sleep(move_time)
			self.stop_wait()

	


	def move_backward(self, speed, move_time=0):		#speed =0 for low and 1 med, 2 high
		if self.car_move_status not in [self.__CAR_STOP, self.__CAR_BACKWARD]: self.stop_wait()
		self.right_wheel.set_dir_power(1, self.__MOVE_BACKWARD[speed][0])
		self.left_wheel.set_dir_power(1, self.__MOVE_BACKWARD[speed][1])
		self.car_move_status = self.__CAR_BACKWARD
		if move_time!=0:
			time.sleep(move_time)
			self.stop_wait()

	def turn_90(self,direction): # direction=0 for CW and 1 for CCW
		self.stop_wait()
		self.right_wheel.set_dir_power((1,0)[direction], self.__TURN_90[1])
		self.left_wheel.set_dir_power((0,1)[direction], self.__TURN_90[2])
		self.car_move_status = self.__CAR_TURN
		time.sleep(self.__TURN_90[0])
		self.stop_wait()
		self.car_move_status = self.__CAR_STOP
		pass

	def turn_180(self, direction):  # direction=0 for CW and 1 for CCW
		self.stop_wait()
		self.right_wheel.set_dir_power((1,0)[direction], self.__TURN_180[1])
		self.left_wheel.set_dir_power((0,1)[direction], self.__TURN_180[2])
		self.car_move_status = self.__CAR_TURN
		time.sleep(self.__TURN_180[0])
		self.stop_wait()
		self.car_move_status = self.__CAR_STOP
		pass

	def stop_wait(self):
		self.right_wheel.stop()
		self.left_wheel.stop()
		time.sleep(0.5)
		self.car_move_status = self.__CAR_STOP


#++self testing routine ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def main():
	car=car_simple_drive(debug=True)

	car.move_forward(0,5)

	car.move_backward(0,5)
	#car.turn_90(0)
	'''

	for i in range(1000,4000,300):
		car.move(1, i, i)
		time.sleep(2)
		print "moving at power: "+str(i)
	car.stop_wait()

	time.sleep(2)
	for i in range(1000,4000,300):
		car.move(-1, i, i)
		time.sleep(2)
		print "moving at power: "+str(i)
	'''
	#time.sleep(5)
	#car.stop_wait()

if __name__ == '__main__':
	main()



