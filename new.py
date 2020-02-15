from apiclient.discovery import build # used for getting data from youtube through their api
from datetime import datetime # used for the time stamp on the data reports
import secret # holds the api key
import time

youtube = build('youtube', 'v3', developerKey=secret.YOUTUBE_API_KEY) #allows us to use the api using our api key

def ReportData(self, _liveSubscribers, _liveViews, _numOfVideos, _averageViewsPerVideo): # prints out the current channel's data
    results = "\nSubscribers: " + str(_liveSubscribers) + "\nViews: " + str(_liveViews) + "\nVideos: " + str(_numOfVideos) + "\nAverage Views Per Video: " + str(_averageViewsPerVideo)
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
        req = youtube.channels().list(part='snippet,contentDetails,statistics', id=self.channelId).execute()
        return req['items'][0]['statistics']

    def UpdateLiveCounts(self):
        channelData = self.GetChannelData()
        self.SubscriberCounter.SetLiveCount(int(channelData['subscriberCount']))
        self.ViewCounter.SetLiveCount(int(channelData['viewCount']))

        self.numOfvideos = int(channelData['videoCount'])
        self.averageViewsPerVideo = self.ViewCounter.liveCount / self.numOfvideos

        ReportData(self, self.SubscriberCounter.liveCount, self.ViewCounter.liveCount, self.numOfvideos, self.averageViewsPerVideo)
        print("Subscriber light should be at " + str(self.SubscriberCounter.GetPercentChange()) + " brightness")
        print("Views light should be at " + str(self.ViewCounter.GetPercentChange()) + " brightness")

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
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(subscriberLightPin, GPIO.OUT)
# GPIO.setup(viewLightPin, GPIO.OUT)
# GPIO.setup(resetBtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#sets up the brightness functionality and starts the lights off at 0% brightness
# subscriberLight = GPIO.PWM(subscriberLightPin, 100)
# viewLight = GPIO.PWM(viewLightPin, 100)
# subscriberLight.start(0)
# viewLight.start(0)

def RunApp(_channelId):
    trackingChannel = Channel(_channelId);


    loopBrakes = 0
    scanFrequency = 60 * 1

    while True:
        time.sleep(.1)
        
        #Listens for button input
        # if(GPIO.input(resetBtnPin) == False): 
        #     print("Reset Button Activated!")

        #     trackingChannel.SubscriberCounter.ResetCounter()
        #     trackingChannel.ViewCounter.ResetCounter()
            
            # subscriberLight.start(trackingChannel.SubscriberCounter.GetPercentChange())
            # viewLight.start(trackingChannel.ViewCounter.GetPercentChange())

        if(time.time() > loopBrakes):
            trackingChannel.UpdateLiveCounts()

            loopBrakes = time.time() + scanFrequency #makes the loop happen x seconds later

RunApp('UCT5_uqXPSVUaL5r2ChcBVeg')