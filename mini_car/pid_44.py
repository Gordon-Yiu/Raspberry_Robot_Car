'''
PID_44.py  : 
class PID_44 for 4
a modification of original pid.py from cnr437@gmail.com
0. initialize and set target in the same time.
my own solution for too small value of encoder per 0.25s. There are only 5~10 pulses.
Therefore I collect 4 values in 1 seconds and then subtract the 0th from 4th.

class PID_1 for 1
0. initialize and set target in the same time.
1. subclass PID, debug its parameter
2. compute the increment and update to PID.
'''
from pid import PID

class PID_44(PID):
  '''
  subclass PID


  '''
  def __init__(self, P=2.0, I=0.0, D=1.0, Derivator=0, Integrator=0, \
    Integrator_max=500, Integrator_min=-500, set_point=10):
    print "in pid44: ", P,I,D

    self.current=[0, 0, 0, 0, 0]
    self.data_number=0

    PID.__init__(self, P, I, D, Derivator=0, Integrator=0, \
      Integrator_max=500, Integrator_min=-500)
    PID.setPoint(self, set_point)

  def update(self, current_value):
    if self.data_number < 5:
      self.current[self.data_number]=current_value
      if self.data_number==0:
        effective_current_value=current_value * 4.0
      else: 
        effective_current_value=4.0* (self.current[self.data_number]-\
          self.current[0]) /(self.data_number)
      self.data_number += 1
      print effective_current_value

      return PID.update(self, effective_current_value)
    else:
      self.current=[self.current[1], self.current[2], self.current[3],\
      self.current[4], current_value]
      print "current array: ", self.current
      print "error value: ", self.current[4]-self.current[0]

      return PID.update(self, self.current[4]-self.current[0])

#++monitoring operation of PID++++++++++++++++++++++++++++++++++++++++++++
class PID_1(PID):
  '''
  subclass PID but for debug purpose, just use directly.

  '''
  def __init__(self, P=2.0, I=0.0, D=1.0, Derivator=0, Integrator=0, \
    Integrator_max=500, Integrator_min=-500, set_point=10):
    '''
    initial
    '''
    print "in pid_1: input parameters ", P,I,D,set_point, "to init PID"
    self.count=0

    PID.__init__(self, P, I, D, Derivator, Integrator, \
      Integrator_max, Integrator_min)
    PID.setPoint(self, set_point)

  def update(self, current_value):
    '''
    we take the increment each time and update this to pid.update()
    remember this:
    We set the target as a increment per second (or in certain timeslot).
    Therefore we need to take calculate the increment and then update to pid class.

    '''
    print "in pid_1: current_value:---", current_value, \
    "-setpoint:--", self.set_point

    a, b, c, d, e=PID.update(self, current_value)
    print "in pid_1, returned from PID: ", a,b,c,d,e
    return a, b, c, d, e



