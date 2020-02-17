# ~ ~ ~ Youtube Channel Tracker ~ ~ ~
# Prints out basic data from a single channel and notifies you of any channel growth with LED lights
# Author: Lucidreline


from apiclient.discovery import build # used for getting data from youtube through their api
from datetime import datetime # used for the time stamp on the data reports
import RPi.GPIO as GPIO # lets us use the led lights and button
import config # holds the api key, the channel I want to track, etc

import time

try:
    youtube = build('youtube', 'v3', developerKey=config.YOUTUBE_API_KEY) #allows us to use the api using our api key
except Exception as e:
    print(e)
    exit()

def ReportData(_channel): # prints out the current channel's data
    results = "\nSubscribers: " + str(_channel.SubscriberCounter.liveCount) + "\nViews: " + str(_channel.ViewCounter.liveCount) + "\nVideos: " + str(_channel.numOfvideos) + "\nAverage Views Per Video: " + str(_channel.averageViewsPerVideo)
    currentTime = datetime.now()

    print("\n ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ")

    print("Date: " + str(currentTime.month) + "/" + str(currentTime.day) + "/" + str(currentTime.year))  
    print("Time: " + str(currentTime.hour) + ":" + str(currentTime.minute) + ":" + str(currentTime.second) + "\n") 
    print(results)

    print(" ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ \n")

class Channel:
    def __init__(self, _channelId):
        self.channelId = _channelId
        self.channelData = self.GetChannelData()

        self.numOfsubscribers = int(self.channelData['subscriberCount'])
        self.numOfvideos = int(self.channelData['videoCount'])
        self.numOfViews = int(self.channelData['viewCount'])

        self.averageViewsPerVideo = self.numOfViews / self.numOfvideos

        self.SubscriberCounter = self.Counter(self.numOfsubscribers, self.numOfsubscribers)
        self.ViewCounter = self.Counter(self.numOfViews, self.numOfViews)
    
    def GetChannelData(self):
        try:
            req = youtube.channels().list(part='snippet,contentDetails,statistics', id=self.channelId).execute()
            return req['items'][0]['statistics']
        except:
            print("Failed to get youtube data. Trying again in a bit...")

    def UpdateLiveCounts(self):
        channelData = self.GetChannelData()
        self.SubscriberCounter.SetLiveCount(int(channelData['subscriberCount']))
        self.ViewCounter.SetLiveCount(int(channelData['viewCount']))

        self.numOfvideos = int(channelData['videoCount'])
        self.averageViewsPerVideo = self.ViewCounter.liveCount / self.numOfvideos

        ReportData(self)

    class Counter:
        def __init__(self, _liveCount, _countSinceReset, _goal = 10):
            self.liveCount = _liveCount
            self.countSinceReset = _countSinceReset
            self.changeInCount = 0
            self.goal = _goal
        
        def SetLiveCount(self, _newLiveCount):
            self.liveCount = _newLiveCount
            self.changeInCount = self.liveCount - self.countSinceReset

        def ResetCounter(self):
            self.countSinceReset = self.liveCount
            self.changeInCount = 0
        
        def GetPercentChange(self):
            percentChange = (self.changeInCount/self.goal) * 100
            if(percentChange < 0.0): # I dont want a negative percent change
                return 0
            else:
                return percentChange

        

subscriberLightPin = 4
viewLightPin = 17
resetBtnPin = 26

#This sets up the pins on the RPi
GPIO.setmode(GPIO.BCM)
GPIO.setup(subscriberLightPin, GPIO.OUT)
GPIO.setup(viewLightPin, GPIO.OUT)
GPIO.setup(resetBtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#sets up the brightness functionality and starts the lights off at 0% brightness
subscriberLight = GPIO.PWM(subscriberLightPin, 100)
viewLight = GPIO.PWM(viewLightPin, 100)
subscriberLight.start(100)
viewLight.start(100)
time.sleep(3)
subscriberLight.start(0)
viewLight.start(0)


banner = """
  ██▓     █    ██  ▄████▄   ██▓▓█████▄  ██▀███  ▓█████  ██▓     ██▓ ███▄    █ ▓█████ 
 ▓██▒     ██  ▓██▒▒██▀ ▀█  ▓██▒▒██▀ ██▌▓██ ▒ ██▒▓█   ▀ ▓██▒    ▓██▒ ██ ▀█   █ ▓█   ▀ 
 ▒██░    ▓██  ▒██░▒▓█    ▄ ▒██▒░██   █▌▓██ ░▄█ ▒▒███   ▒██░    ▒██▒▓██  ▀█ ██▒▒███   
 ▒██░    ▓▓█  ░██░▒▓▓▄ ▄██▒░██░░▓█▄   ▌▒██▀▀█▄  ▒▓█  ▄ ▒██░    ░██░▓██▒  ▐▌██▒▒▓█  ▄ 
 ░██████▒▒▒█████▓ ▒ ▓███▀ ░░██░░▒████▓ ░██▓ ▒██▒░▒████▒░██████▒░██░▒██░   ▓██░░▒████▒
 ░ ▒░▓  ░░▒▓▒ ▒ ▒ ░ ░▒ ▒  ░░▓   ▒▒▓  ▒ ░ ▒▓ ░▒▓░░░ ▒░ ░░ ▒░▓  ░░▓  ░ ▒░   ▒ ▒ ░░ ▒░ ░
 ░ ░ ▒  ░░░▒░ ░ ░   ░  ▒    ▒ ░ ░ ▒  ▒   ░▒ ░ ▒░ ░ ░  ░░ ░ ▒  ░ ▒ ░░ ░░   ░ ▒░ ░ ░  ░
   ░ ░    ░░░ ░ ░ ░         ▒ ░ ░ ░  ░   ░░   ░    ░     ░ ░    ▒ ░   ░   ░ ░    ░   
       ░  ░   ░     ░ ░       ░     ░       ░        ░  ░    ░  ░ ░           ░    ░  ░
                 ░             ░                                                    
"""

def RunApp(_channelId):

    print(banner)
    trackingChannel = Channel(_channelId);

    loopBrakes = 0
    scanFrequency = 60 * 1

    while True:
        time.sleep(.1)
        
        #Listens for button input
        if(GPIO.input(resetBtnPin) == False): 
            print("Reset Button Activated!")

            trackingChannel.SubscriberCounter.ResetCounter()
            trackingChannel.ViewCounter.ResetCounter()
            
            subscriberLight.start(trackingChannel.SubscriberCounter.GetPercentChange())
            viewLight.start(trackingChannel.ViewCounter.GetPercentChange())

        if(time.time() > loopBrakes):
            trackingChannel.UpdateLiveCounts()
            loopBrakes = time.time() + scanFrequency #makes the loop happen x seconds later


RunApp(config.ChannelToTrack)
