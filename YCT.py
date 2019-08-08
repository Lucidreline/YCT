import urllib.request
import json
import time
import datetime
import RPi.GPIO as GPIO


#gets the current time


scanFrequency = 60 #these are in seconds
loopBrakes    = 0
#these control the scan loops. Prevents the scans to be too  frequent


#sets the pin numbers from the RPi
subLightPin = 4
viewLightPin = 17
buttonPin = 26

#This sets up the pins on the RPi
GPIO.setmode(GPIO.BCM)
GPIO.setup(subLightPin, GPIO.OUT)
GPIO.setup(viewLightPin, GPIO.OUT)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#sets up the brightness functionality and starts the lights off at 0% brightness
subPWM = GPIO.PWM(subLightPin, 100)
viewPWM = GPIO.PWM(viewLightPin, 100)
subPWM.start(0)
viewPWM.start(0)

key = "AIzaSyD9xf4yeziXrBDuNgSimq9XarHmVvmHDgs"
#got this from google APIs
#Hard coded url: https://www.googleapis.com/youtube/v3/channels?part=statistics&id=UCT5_uqXPSVUaL5r2ChcBVeg&key=AIzaSyD9xf4yeziXrBDuNgSimq9XarHmVvmHDgs

class channel:
    def __init__(self, name, id, subGoal, viewGoal):
        self.name   = name
        self.id     = id
        self.videos = 0
        self.subs   = self.subCount(0, 0, subGoal)
        self.views  = self.viewCount(0, 0, 0, viewGoal)

    class subCount:
        def __init__(self, current, original, goal):
            self.current  = current
            self.original = original
            self.increase = current - original
            self.goal     = goal

    class viewCount:
        def __init__(self, current, original, average, goal):
            self.current  = current
            self.original = original 
            self.increase = current - original
            self.average  = average
            self.goal     = goal
#this is a big object incase I ever want to track multiple channels           


def getThemSubs(_channel):
    data = urllib.request.urlopen("https://www.googleapis.com/youtube/v3/channels?part=statistics&id=" + _channel.id +"&key=" + key).read()
    _channel.subs.current = json.loads(data)["items"][0]["statistics"]["subscriberCount"]
    #this gets the number of subscribers that the channel has


def getThemViews(_channel):
    data = urllib.request.urlopen("https://www.googleapis.com/youtube/v3/channels?part=statistics&id=" + _channel.id +"&key=" + key).read()
    _channel.views.current = json.loads(data)["items"][0]["statistics"]["viewCount"]
    _channel.videos = json.loads(data)["items"][0]["statistics"]["videoCount"]
    #this gets the number of total views and videos

    _channel.views.current = int(_channel.views.current)
    _channel.videos = int(_channel.videos)
    _channel.views.average = _channel.views.current/_channel.videos * 1.0 
    #uses the previous information to find the average ammount of views per video

def TimeStamp():
    currentTime = datetime.datetime.now()
    print("Date: " + str(currentTime.month) + "/" + str(currentTime.day) + "/" + str(currentTime.year))  
    print("Time: " + str(currentTime.hour) + ":" + str(currentTime.minute) + ":" + str(currentTime.second) + "\n") 
     

def Scan(_channel):
    TimeStamp()
    getThemSubs(_channel)
    getThemViews(_channel)
    #this just calls the methods


def DebugPrints(_channel):
    print(_channel.name + "\'s current subs    : "      + str(_channel.subs.current))
    print(_channel.name + "\'s original subs   : "     + str(_channel.subs.original))
    print(_channel.name + "\'s increase in subs: "  + str(_channel.subs.increase))

    print("  ")

    print(_channel.name + "\'s current views    : "     + str(_channel.views.current))
    print(_channel.name + "\'s original views   : "    + str(_channel.views.original))
    print(_channel.name + "\'s increase in views: " + str(_channel.views.increase))
    #prints information to help me debug in the future
   
    
def ProcessIncreases(_channel):
    if(_channel.subs.increase > 0):
        print("\nNEW SUBSCRIBER for " + _channel.name + "\'S CHANNEL!!\n")
        
    subsBrightness = (_channel.subs.increase/_channel.subs.goal) * 100
    print("\nSubs light : " + str(subsBrightness) + "% brightness" )
    #This determines how bright the light will be
    if(subsBrightness < 0):
        subsBrightness = 0
    subPWM.start(subsBrightness)
    #sets the light brightness


    if(_channel.views.increase > 0):
        print("\nNEW VIEW for " + _channel.name + "\'S CHANNEL!!\n")

    viewsBrightness = (_channel.views.increase/_channel.views.goal) * 100
    print("Views light: " + str(viewsBrightness) + "% brightness" )
    if(viewsBrightness < 0):
        viewsBrightness = 0
    viewPWM.start(viewsBrightness)


    

def AnalyzeChannel(_channel):

    #the goal controls how bright the light will be. If you meet/exceed the goal then the light will be lit at the max

    Scan(_channel)
    #gets the number of subscribers & views


    #Initial print
    print(_channel.name + " has " + "{:,d}".format(int(_channel.subs.current)) + " subscribers!")
    print(_channel.name + " has " + "{:,d}".format(int(_channel.views.current)) + " total views!")
    print(_channel.name + " has an average of " + str(_channel.views.average) + " views per video")
    #prints what was found in the initial scan


    # give the original counts
    _channel.subs.original  = _channel.subs.current
    _channel.views.original = _channel.views.current


    loopBrakes = 0
    while (1==1):
        time.sleep(.1)

        #Listens for button input
        if(GPIO.input(buttonPin) == False): 
            print("button pressed!")
            _channel.subs.original = _channel.subs.current 
            _channel.views.original = _channel.views.current
            
            subPWM.start(0)
            viewPWM.start(0)

        if(time.time() > loopBrakes):
            print("- - - - - - - - - - - - - - - - - - - - - - - - -")
            Scan(_channel)

            _channel.subs.increase  = int(_channel.subs.current)  - int(_channel.subs.original)
            _channel.views.increase = int(_channel.views.current) - int(_channel.views.original)

            DebugPrints(_channel)

            ProcessIncreases(_channel)

            loopBrakes = time.time() + scanFrequency #makes the loop happen x seconds later

#-----------------------------------
#This is where you add your channel, channel ID, aswell as your subscriber and view goals


            
