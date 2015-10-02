#!/usr/bin/python
'''
log_car.py
generate log file according to message given.
timing-log will log message and timing in the same time


'''
import time
timing_tic=0.0

TIMING_LOG_FILE_NAME    = "timing_log.txt"
MISSION_LOG_FILE_NAME   = "mission_log.txt"
#++timing_log++++++++++++++++++++++++++++++++++++++++++
def timing_log(i, logmessage):
    '''
    function timing_log V1.0
    input: a string as message
    This function log it to file with file name TIMING_LOG_FILE_NAME and time stamp and also delta time.
    '''
    global timing_tic
    with open(TIMING_LOG_FILE_NAME,'a') as f:
        a=time.time()
        tmpstring="%5d, %9.4f, %s, %5.5f, " % (i, a-1441700000, \
                                               time.strftime("%Y-%m-%d, %H:%M:%S",time.localtime(a)) ,\
                                               a-timing_tic) + logmessage + "\n"
        f.write(tmpstring)
        timing_tic=a

#++mission_log++++++++++++++++++++++++++++++++++++++++++
def mission_log(i, logmessage):
    '''
    function mission_log V1.0
    input: a string as message
    This function log it to file with file name MISSION_LOG_FILE_NAME and attach a time stamp.
    '''
    with open(MISSION_LOG_FILE_NAME,'a') as f:
        f.write(str(i).rjust(6)+ ", "+ str(time.time()).rjust(15)+", "+time.ctime(time.time()) + ", "\
                +logmessage+"\n")
