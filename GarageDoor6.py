import RPi.GPIO as GPIO
import time,sys,datetime
import psycopg2
from psycopg2.extras import execute_values import telepot from telepot.loop import MessageLoop
f1 = open ('DoorOutput.txt', 'a')			# Outputfile - CSV
import io
import os

'''
Configure raspberry
'''
GPIO.setmode(GPIO.BOARD)
in1 = 13
in2 = 15
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.output(in1,True)
GPIO.output(in2,True)
button1 = 3
button2 = 5
mayask = "1"


GPIO.setup(button1,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(button2,GPIO.IN,pull_up_down=GPIO.PUD_UP)

f2 = open("/sys/class/thermal/thermal_zone0/temp", "r") t = float(f2.readline ()) CPUTemp = t/1000 '''
Configure some global variables
'''

now = datetime.datetime.now()


tel_starttime = 0
tel_endtime = 0
tel_lastvol = 0
tel_duration = 0
tel_endtime  = datetime.datetime.now()

print('Control C to exit')
print (CPUTemp)

def action(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    print 'Received: %s' % command
    f2 = open("/sys/class/thermal/thermal_zone0/temp", "r")
    t = float(f2.readline ())
    CPUTemp = t/1000  
   
    if command == '/hi':
        telegram_bot.sendMessage (chat_id, str("Hello! 31 La Gratitude Garage ")+str("\n\rStatus: ")+str("\n\r")+str(Door1Status)+str("\n\r")+str(Door2Status)+str("\n\rCPU Temp: ")+str(CPUTemp))
    elif command == '/time':
        telegram_bot.sendMessage(chat_id, str("Bot Start Date: ")+str(now.year)+str("-")+str(now.month)+str("-")+str(now.day)+str("    ")+str(now.hour)+str(":")+str(now.minute) + str("\n\rUpTime: ")+ str(datetime.datetime.now()-now))
    elif command == '/door1':
        GPIO.output(in1,False)
        time.sleep(0.1)
        GPIO.output(in1,True)
        telegram_bot.sendMessage(chat_id, str("Garage Door 1 Moving"))
    elif command == '/door2':
        GPIO.output(in2,False)
        time.sleep(0.1)
        GPIO.output(in2,True)
        telegram_bot.sendMessage(chat_id, str("Garage Door 2 Moving"))
    elif command == '/status':
        if button_state1 == True or button_state2 == True: 
            telegram_bot.sendMessage(550934694, str(Door1Status)+str("\n\r")+str(Door2Status)+str("\n\rMaybe close it now?"))
        else:
            telegram_bot.sendMessage(550934694, str(Door1Status)+str("\n\r")+str(Door2Status)+str("\n\rAll is Good!"))
    elif command == '/data':
        telegram_bot.sendDocument(chat_id, document=open('/home/pi/GarageDoor/DoorOutput.txt'))
    elif command == '/source':
        telegram_bot.sendDocument(chat_id, document=open('/home/pi/GarageDoor/GarageDoor6.py'))
    elif command == '/ip':
        os.system("curl ifconfig.co > currentip.txt")
        telegram_bot.sendDocument(chat_id, document=open('/home/pi/GarageDoor/currentip.txt'))




telegram_bot = telepot.Bot('Your Bot ID here')
print (telegram_bot.getMe())


MessageLoop(telegram_bot, action).run_as_thread() print 'Up and Running....'

telegram_bot.sendMessage (Your Chat-ID here, str("Hello! 31 La Gratitude Garage Bot Started"))



while True:

    '''
    This is what actually runs the whole time. 

    '''

    button_state1 = GPIO.input(button1)
    if button_state1 == True:
        Door1Status = 'Door1 is Open'
#        print Door1Status
    else:
        Door1Status = 'Door1 is Closed'
#        print Door1Status

    button_state2 = GPIO.input(button2)
    if button_state2 == True:
        Door2Status = 'Door2 is Open'
#        print Door2Status
    else:
        Door2Status = 'Door2 is Closed'
#        print Door2Status
    

    if datetime.datetime.now().strftime('%H:%M') == '18:29':
        time.sleep(70)
        mayask = "1"
    if datetime.datetime.now().strftime('%H:%M') == '18:59':
        time.sleep(70)
        mayask = "1"
    if datetime.datetime.now().strftime('%H:%M') == '19:29':
        time.sleep(70)
        mayask = "1"



#    print datetime.datetime.now().strftime('%H:%M')    
    if mayask == "1":
        if button_state1 == True or button_state2 == True: 
            telegram_bot.sendMessage(Your Chat-ID here, str(Door1Status)+str("\n\r")+str(Door2Status)+str("\n\rMaybe close it now?"))
            mayask = "0"
        else:
            telegram_bot.sendMessage(Your Chat-ID here, str(Door1Status)+str("\n\r")+str(Door2Status)+str("\n\rAll is Good!"))
            mayask = "0"            




'''
This last part simply prints some helpful information. It also allows for a clean exit if user presses Ctrl + C.
'''
try:
        print('All Done ')
except KeyboardInterrupt:
        print('\nCTRL C - Exiting nicely')
        f1.close()
        GPIO.cleanup()
        sys.exit()
