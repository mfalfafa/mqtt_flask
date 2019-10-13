import RPi.GPIO as GPIO

import time
import threading
import paho.mqtt.client as mqtt
from flask import Flask
from flask_ask import Ask, statement

pins={"red":3, "yellow":4, "green":17}

app=Flask(__name__)
ask=Ask(app, '/')

@ask.intent('LedIntent')
def led(color, status):
  if color.lower() not in pins.keys():
     return statement("I don't have {} light".format(color))
  GPIO.output(pins[color], GPIO.HIGH if status == "on" else GPIO.LOW)
  return statement("Turning the {} light {}".format(color, status))

turn_off_alarm=0
turn_off_pir=0
turn_off_door=0
door_status=0
ready=0
start=0

GPIO.setmode(GPIO.BCM)

# buzzer/alarm
alarm=2
GPIO.setup(2, GPIO.OUT)
GPIO.output(2, 1)
# lamp1
lamp1=3
GPIO.setup(3, GPIO.OUT)
GPIO.output(3, 1)
#lamp2
lamp2=4
GPIO.setup(4, GPIO.OUT)
GPIO.output(4, 1)
#lamp3
lamp3=17
GPIO.setup(17, GPIO.OUT)
GPIO.output(17, 1)

# green led
plug_led=22
GPIO.setup(22, GPIO.OUT)
GPIO.output(22, 0)
# smart plug
plug=9
GPIO.setup(9, GPIO.OUT)
GPIO.output(9, 0)
# kipas
kipas=10
GPIO.setup(10, GPIO.OUT)
GPIO.output(10, 0)
# led pir
led_pir=26
GPIO.setup(26, GPIO.OUT)
GPIO.output(26, 0)

# variable
alarmThread=""
ledPirThread=""
ledPlugThread=""
lamp1Thread=""
lamp2Thread=""
lamp3Thread=""
sendDataThread=""

####### CALLBACK IN #######
def pb_plug_event(self):
   print("PLUG NOISE")
   time.sleep(0.2)
   if GPIO.input(pb_plug)==1:
      print("PB PLUG PRESS")
def pir_event(self):
   print("PIR")
   #time.sleep(2)
def pb_lamp1_event(self):
   print("PB LAMP1 PRESS")
   if GPIO.input(lamp1)==1:
      #lamp1 off
      #turn on lamp1
      GPIO.output(lamp1, 0)
   else:
      GPIO.output(lamp1, 1)
   time.sleep(0)

def pb_lamp2_event(self):
   print("PB LAMP2 PRESS")
   if GPIO.input(lamp2)==1:
      #lamp2 off
      #turn on lamp2
      GPIO.output(lamp2, 0)
   else:
      GPIO.output(lamp2, 1)
   time.sleep(0)
def pb_lamp3_event(self):
   print("PB LAMP3 PRESS")
   if GPIO.input(lamp3)==1:
      #lamp3 off
      #turn on lamp3
      GPIO.output(lamp3, 0)
   else:
      GPIO.output(lamp3, 1)
   time.sleep(0)
def pb_pir_event(self):
   print("PIR NOISE")
   print(GPIO.input(pb_pir))
   time.sleep(0.2)
   if GPIO.input(pb_pir)==1:
      print("PB PIR PRESS")

####### INPUT #######
#door sensor
door=21
GPIO.setup(door, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# button plug
pb_plug=27
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# pir sensor
sen_pir=11
GPIO.setup(11, GPIO.IN)
#GPIO.add_event_detect(11, GPIO.RISING)
#GPIO.add_event_callback(11, pir_event)
# pb lamp1
pb_lamp1=5
GPIO.setup(5, GPIO.IN)
# PB LAMP2
pb_lamp2=6
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(6, GPIO.RISING)
GPIO.add_event_callback(6, pb_lamp2_event)
# pb lamp3
pb_lamp3=13
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(13, GPIO.RISING)
GPIO.add_event_callback(13, pb_lamp3_event)
# pb pir
pb_pir=19
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def on_connect(mqttc, obj, flags, rc):
   print("rc: "+ str(rc))
def on_message(mqttc, obj, msg):
   global turn_off_alarm, turn_off_pir, turn_off_door, ready, start
   print(msg.topic+ " "+ str(msg.payload))
   if ready==1 or start>=17:
      if msg.topic=="turn_on_lamp1":
         print(msg.topic)
         GPIO.output(lamp1, 0)
      elif msg.topic=="turn_on_lamp2":
         print(msg.topic)
         GPIO.output(lamp2, 0)
      elif msg.topic=="turn_on_lamp3":
         print(msg.topic)
         GPIO.output(lamp3, 0)
      elif msg.topic=="turn_on_plug":
         print(msg.topic)
         GPIO.output(plug, 1)
      elif msg.topic=="turn_on_fan":
         print(msg.topic)
         GPIO.output(kipas, 1)
      elif msg.topic=="turn_on_alarm":
         print(msg.topic)
         turn_off_alarm=0
      elif msg.topic=="turn_off_lamp1":
         print(msg.topic)
         GPIO.output(lamp1, 1)
      elif msg.topic=="turn_off_lamp2":
         print(msg.topic)
         GPIO.output(lamp2, 1)
      elif msg.topic=="turn_off_lamp3":
         print(msg.topic)
         GPIO.output(lamp3, 1)
      elif msg.topic=="turn_off_plug":
         print(msg.topic)
         GPIO.output(plug, 0)
      elif msg.topic=="turn_off_fan":
         print(msg.topic)
         GPIO.output(kipas, 0)
      elif msg.topic=="turn_off_alarm":
         print(msg.topic)
         turn_off_alarm=1
      elif msg.topic=="turn_off_pir":
         turn_off_pir=1
      elif msg.topic=="turn_on_pir":
         turn_off_pir=0
      elif msg.topic=="turn_on_door":
         turn_off_door=0
      elif msg.topic=="turn_off_door":
         turn_off_door=1
   #start += 1

def on_publish(mqttc, obj, mid):
   print("publish "+ str(mid))
def on_subscribe(mqttc, obj, mid, granted_qos):
   print("Subscribed: "+ str(mid)+ " "+ str(granted_qos))
def on_log(mqttc, obj, level, string):
   print(string)
def on_disconnect(client, userdata, rc):
   print("Disconnect: "+ str(rc))

mqttc=mqtt.Client()
mqttc.on_message=on_message
mqttc.on_connect=on_connect
mqttc.on_publish=on_publish
mqttc.on_subscribe=on_subscribe
mqttc.on_disconnect=on_disconnect

ready_f=0
while 1:
   try:
      mqttc.connect("127.0.0.1", 1883, 60)
      ready_f=1
   except:
      print("Waiting for the server...")
      time.sleep(1)
   if ready_f==1:
      break

mqttc.subscribe("turn_on_plug")
mqttc.subscribe("turn_off_plug")
mqttc.subscribe("turn_on_lamp1")
mqttc.subscribe("turn_off_lamp1")
mqttc.subscribe("turn_on_lamp2")
mqttc.subscribe("turn_off_lamp2")
mqttc.subscribe("turn_on_lamp3")
mqttc.subscribe("turn_off_lamp3")
mqttc.subscribe("turn_on_fan")
mqttc.subscribe("turn_off_fan")
mqttc.subscribe("turn_off_alarm")
mqttc.subscribe("turn_on_alarm")
mqttc.subscribe("turn_off_pir")
mqttc.subscribe("turn_on_pir")
mqttc.subscribe("turn_off_door")
mqttc.subscribe("turn_on_door")

class sendDataThread(threading.Thread):
   def __init__(self):
      threading.Thread.__init__(self)
   def run(self):
      sendData()
def sendData():
   global door_status
   while 1:
      mqttc.publish("get_lamp1_data", str(GPIO.input(lamp1)))
      mqttc.publish("get_lamp2_data", str(GPIO.input(lamp2)))
      mqttc.publish("get_lamp3_data", str(GPIO.input(lamp3)))
      mqttc.publish("get_pir_data", str(GPIO.input(sen_pir)))
      mqttc.publish("get_plug_data", str(GPIO.input(plug)))
      mqttc.publish("get_alarm_data", str(GPIO.input(alarm)))
      mqttc.publish("get_fan_data", str(GPIO.input(kipas)))
      mqttc.publish("get_door_data", str(door_status))
      mqttc.publish("get_pir_control_status", str(1 if turn_off_pir==0 else 0))
      mqttc.publish("get_alarm_control_status", str(1 if turn_off_alarm==0 else 0))
      mqttc.publish("get_door_control_status", str(1 if turn_off_door==0 else 0))
      time.sleep(0.1)

class lamp2Thread(threading.Thread):
   def __init__(self):
      threading.Thread.__init__(self)
   def run(self):
      lamp2Event()
def lamp2Event():
   while 1:
      if GPIO.input(pb_lamp2)==1:
         time.sleep(0.1)
         if GPIO.input(pb_lamp2)==1:
            if GPIO.input(lamp2)==1:
               #lamp2 off
               #turn on lamp2
               GPIO.output(lamp2, 0)
            else:
               GPIO.output(lamp2, 1)
         while GPIO.input(pb_lamp2)==1:
            pass
class lamp1Thread(threading.Thread):
   def __init__(self):
      threading.Thread.__init__(self)
   def run(self):
      lamp1Event()
def lamp1Event():
   while 1:
      if GPIO.input(pb_lamp1)==1:
         time.sleep(0.1)
         if GPIO.input(pb_lamp1)==1:
            if GPIO.input(lamp1)==1:
               #lamp1 off
               #turn on lamp1
               GPIO.output(lamp1, 0)
            else:
               GPIO.output(lamp1, 1)
         while GPIO.input(pb_lamp1)==1:
            pass
class ledPlugThread(threading.Thread):
   def __init__(self):
      threading.Thread.__init__(self)
   def run(self):
      ledPlugEvent()
def ledPlugEvent():
   while 1:
      if GPIO.input(pb_plug)==1:
         time.sleep(0.1)
         if GPIO.input(pb_plug)==1:
            print("PB PLUG PRESSED")
            #turn on led plug
            f=0
            for i in range(21):
               f=~f
               GPIO.output(plug_led, f)
               time.sleep(0.7)
class ledPirThread(threading.Thread):
   def __init__(self):
      threading.Thread.__init__(self)
   def run(self):
      ledPirEvent()
def ledPirEvent():
   while 1:
      if GPIO.input(pb_pir)==1:
         time.sleep(0.1)
         if GPIO.input(pb_pir)==1:
            print("PB PIR PRESSED")
            #led pir off
            #turn on led pir
            f=0
            for i in range(21):
               f=~f
               GPIO.output(led_pir, f)
               time.sleep(0.7)

class alarmThread(threading.Thread):
   def __init__(self):
      threading.Thread.__init__(self)
   def run(self):
      alarmEvent()
def alarmEvent():
   global turn_off_alarm, turn_off_pir, alarm
   while 1:
      f=0
      if turn_off_pir==0:
         # alarm for safety using pir sensor
         while GPIO.input(11)==1:
            print("PIR")
            if turn_off_alarm==0:
               GPIO.output(alarm,0)
            elif turn_off_alarm==1:
               GPIO.output(alarm,1)
            #time.sleep(0.1)
         #if turn_off_alarm==0:
         #   GPIO.output(alarm,0)
         #elif turn_off_alarm==1:
         #   GPIO.output(alarm,1)
         if GPIO.input(11)==0:
            print("PIR 0")
            GPIO.output(alarm,1)
      while turn_off_pir==1:
         if f==0:
            f=1
            print("pir is turned off")

class FlaskThread(Thread):
    def run(self):
        app.run(
            host='127.0.0.1', port=5000, debug=True, use_debugger=True,
            use_reloader=False)

#class webserverThread(threading.Thread):
#   def __init__(self):
#      threading.Thread.__init__(self)
#   def run(self):
#      global app
#      app.run(debug=True)

class doorThread(threading.Thread):
   def __init__(self):
      threading.Thread.__init__(self)
   def run(self):
      doorRun()
def doorRun():
   global door_status, turn_off_alarm
   while 1:
      # alarm for safety using pir sensor
      f=0
      while GPIO.input(door)==1:
         if f==0:
            f=1
            print("DOOR")
            door_status="close"
            GPIO.output(alarm,1)
            time.sleep(0.1)
      f=0
      while GPIO.input(door)==0:
         if f==0:
            f=1
            print("DOOR 2")
            door_status="open"
         if turn_off_alarm==0:
            GPIO.output(alarm,0)
         elif turn_off_alarm==1:
            GPIO.output(alarm,1)
         time.sleep(0.1)


try:
   #webserverThread=webserverThread()
   doorThread=doorThread()
   alarmThread=alarmThread()
   ledPirThread=ledPirThread()
   ledPlugThread=ledPlugThread()
   lamp1Thread=lamp1Thread()
   sendDataThread=sendDataThread()
except Exception as e:
   print("Error: unable to start thread")
# start thread
doorThread.start()
alarmThread.start()
ledPirThread.start()
ledPlugThread.start()
lamp1Thread.start()
sendDataThread.start()
#webserverThread.start()

print("REady----------------------------------------------------")
ready=1
#try:
#   pass
#   app.run(debug=True)
#except:
#   print("ERRR")
#subprocess("ssh -R 80:localhost:5000 serveo.net")
if __name__=='__main__':
   #webserverThread.start()
   server = FlaskThread()
   server.daemon = True
   server.start()
   
   while 1:
      mqttc.loop(timeout=0.001)

GPIO.cleanup()

 
