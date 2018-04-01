# coding:utf-8
#!/usr/bin/python
# System module
import socket
import time
import sys
import requests
import RPi.GPIO as GPIO
import threading
import queue

rbnom=str(socket.gethostname())
cb=""
    
# Set up some global variables
encore = True
time_sleep_led=5
time_sleep_relay=1
time_boucle=1
redPin=23
greenPin=18
relaisPin = 21
q = queue.Queue()

srv_adress_ip="192.168.1.219"

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(redPin, GPIO.OUT)
GPIO.setup(greenPin, GPIO.OUT)
GPIO.setup(relaisPin, GPIO.OUT)
##
##def turnOff(pin):
##    GPIO.setmode(GPIO.BCM)
##    GPIO.setwarnings(False)
##    GPIO.setup(pin, GPIO.OUT)
##    GPIO.output(pin, False)
    
##def turnOn(pin):
##    GPIO.setmode(GPIO.BCM)
##    GPIO.setwarnings(False)
##    GPIO.setup(pin, GPIO.OUT)
##    GPIO.output(pin,True)
##
def turnOn(pin):
    GPIO.output(pin,True)
    time.sleep(time_sleep_led)
    GPIO.output(pin,False)
    
##def redOn():
##	blink(redPin)
##	
##def greenOn():
##	blink(greenPin)   
##
##def bluegreenOn():
##	blink(bluegreenPin)
##	
##def blueredOn():
##	blink(blueredPin)	
##	
##def redOff():
##	turnOff(redPin)
##	
##def greenOff():
##	turnOff(greenPin)
##	
##def bluegreenOff():
##	turnOff(bluegreenPin)
##	
##def blueredOff():
##	turnOff(blueredPin)

def LED_Blink(Kel_led):
    iLed = threading.local()
    iLed.i = 0
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(Kel_led, GPIO.OUT)
    while (iLed.i <= 25):
        GPIO.output(Kel_led, True)
        time.sleep(0.1)   
        GPIO.output(Kel_led, False)
        time.sleep(0.1)
        iLed.i = iLed.i + 1
        
def LED_Blink_Fast(Kel_led):
    iLed = threading.local()
    iLed.i = 0
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(Kel_led, GPIO.OUT)
    while (iLed.i <= 50):
        GPIO.output(Kel_led, True)
        time.sleep(0.05)   
        GPIO.output(Kel_led, False)
        time.sleep(0.05)
        iLed.i = iLed.i + 1
        

def declencherelay():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(relaisPin, GPIO.OUT)
    GPIO.output(relaisPin, True)
    time.sleep(time_sleep_relay)#attend 1 secondes sans rien faire
    GPIO.output(relaisPin, False)
##
def worker():
    oldcb =""
    while 1:
       
        #Lecteur code barre python
        codebarre=sys.stdin.readline().rstrip('\n')
        #print(codebarre)
        if(codebarre != oldcb):
            # oldcb=codebarre
            #Put codebarre into the queue
            q.put(codebarre)
        #else:
            #logging.debug('No value yet')
            #print(codebarre, " : previous read")
                
#queues = []
            

# crée le thread  
w = threading.Thread(name='worker', target=worker)
# démarre le thread 
w.start()


while 1:
    
    if not q.empty():
         
        if(cb == "") and (q.qsize()>0):
            cb=q.get()
        #print('scan code:')
        #Lecteur code barre python
        #codebarre=sys.stdin.readline().rstrip('\n')
        if(cb != ""):
            url="http://"+srv_adress_ip+"/CHECK/"+rbnom+":"+cb
            content=requests.get(url)
            codebarre=cb
            if(content.text.find('OK')!=(-1)):
                #print(cb,' : OK ')
                print(time.asctime(time.localtime(time.time())), ' > CB:', cb, ' : OK ')
               # greenOn()
                #DECLENCHER RELAIS
                t = threading.Thread(name='declencherelay', target=declencherelay).start()
                #time.sleep(time_sleep_led)
                turnOn(greenPin)
                #greenOff()
                cb=""
            elif (content.text.find('NEAR')!=(-1)):
                #print(cb,' : NEAR')
                print(time.asctime(time.localtime(time.time())), ' > CB:', cb, ' : NEAR')
                LED_Blink(greenPin)
                cb=""
            elif (content.text.find('BAD')!=(-1)):    
                 #pwhile 1:rint(cb,' : BAD')
                 print(time.asctime(time.localtime(time.time())), ' > CB:', cb, ' : BAD')            
                 LED_Blink(redPin)               
                 #turnOn(redPin)
                 cb=""    
            else:
                print(time.asctime(time.localtime(time.time())), ' > CB:', cb, ' : ', content.text, ' : ERROR: ')
                LED_Blink_Fast(redPin)
    else:
        print(time.asctime(time.localtime(time.time())), ' > None')
        time.sleep(time_boucle)
    
    
       
           
            