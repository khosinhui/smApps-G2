import pigpio
import RPi.GPIO as GPIO
import time
from Adafruit_CharLCD import Adafruit_CharLCD
from firebase import firebase

# connect to the 
pi = pigpio.pi()

# instantiate lcd and specify pins
lcd = Adafruit_CharLCD(rs=26, en=19,
                       d4=13, d5=6, d6=5, d7=11,
                       cols=16, lines=2)

lcd.clear()

sensor1 = 23
sensor2 = 18

GPIO.setmode(GPIO.BCM)

GPIO.setup(sensor1,GPIO.IN)
GPIO.setup(sensor2,GPIO.IN)

firebase = firebase.FirebaseApplication('https://login-f0a7b.firebaseio.com/', None)
firebase.put('https://login-f0a7b.firebaseio.com/Barrier','servo_in',False)
firebase.put('https://login-f0a7b.firebaseio.com/Barrier','servo_out',False)

lcd.message('READY')
time.sleep(1)
lcd.set_cursor(0,0)#col,row (start with 0-1 for row, col 0-15)
lcd.message('    Welcome!\n   ==smApps==')
time.sleep(1)
pi.set_servo_pulsewidth(25, 1000) # position anti-clockwise
pi.set_servo_pulsewidth(24, 1000) # position anti-clockwise
count=4
lcd.clear()
lcd.message('   ==smApps==')

def entering(count):
    servo_in = firebase.get('https://login-f0a7b.firebaseio.com/Barrier','servo_in')
    if servo_in == True:
        print("open in")
        pi.set_servo_pulsewidth(25, 2000) # position clockwise
        
        if GPIO.input(sensor1):
            pi.set_servo_pulsewidth(25, 1000) # position anti-clockwise
            firebase.put('https://login-f0a7b.firebaseio.com/Barrier','servo_in',False)
            count=count-1
    else:
        print("close in")

    return count         

def leaving(count):
    servo_out = firebase.get('https://login-f0a7b.firebaseio.com/Barrier','servo_out')
    if servo_out == True:
        print("open out")
        pi.set_servo_pulsewidth(24, 2000) # position clockwise
        
        if GPIO.input(sensor2):
            pi.set_servo_pulsewidth(24, 1000) # position anti-clockwise
            firebase.put('https://login-f0a7b.firebaseio.com/Barrier','servo_out',False)
            count=count+1
    else:
        print("close out")

    return count

try:
    while True:
        if count == 0:
            servo_in = firebase.get('https://login-f0a7b.firebaseio.com/Barrier','servo_in')
            if servo_in == True:
                firebase.put('https://login-f0a7b.firebaseio.com/Barrier','servo_in',False)
                lcd.set_cursor(0,1)
                lcd.message("   No Parking")
            count = leaving(count)
            
        else:
            count = entering(count)
            count = leaving(count)

        if GPIO.input(sensor1):
            print("No object at sensor in")
        else:
            print("Object detected at sensor in")
        if GPIO.input(sensor2):
            print("No object at sensor out")
        else:
            print("Object detected at sensor out")
        print()
        lcd.set_cursor(0,1)
        lcd.message("   Parking: ")
        lcd.message(str(count))
        firebase.put('https://login-f0a7b.firebaseio.com/Barrier','Parking_available',count)
        time.sleep(1) 

except KeyboardInterrupt:
    lcd.clear()
    lcd.message('END')
    time.sleep(1)
    GPIO.cleanup()

