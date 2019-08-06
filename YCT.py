import urllib.request
import json
import time

scanFrequency = 60 #these are in seconds
loopBrakes    = 0
#these control the scan loops. Prevents the scans to be too  frequent

key = "AIzaSyD9xf4yeziXrBDuNgSimq9XarHmVvmHDgs"
#got this from google APIs
#Hard coded url: https://www.googleapis.com/youtube/v3/channels?part=statistics&id=UCT5_uqXPSVUaL5r2ChcBVeg&key=AIzaSyD9xf4yeziXrBDuNgSimq9XarHmVvmHDgs

class channel:
    def __init__(self, name, id, videoCount):
        self.name   = name
        self.id     = id
        self.videos = videoCount
        self.subs   = self.subCount(0, 0, 0)
        self.views  = self.viewCount(0, 0, 0, 0)

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

adrianas = channel("Adrianita's channel", "UCT5_uqXPSVUaL5r2ChcBVeg", 1)
adrianas.subs.goal = 10
adrianas.views.goal = 50
    #the goal controls how bright the light will be. If you meet/exceed the goal then the light will be lit at the max
#this created the channel and initialized a few things

def getThemSubs():
    data = urllib.request.urlopen("https://www.googleapis.com/youtube/v3/channels?part=statistics&id=" + adrianas.id +"&key=" + key).read()
    adrianas.subs.current = json.loads(data)["items"][0]["statistics"]["subscriberCount"]
    #this gets the number of subscribers that the channel has

def getThemViews():
    data = urllib.request.urlopen("https://www.googleapis.com/youtube/v3/channels?part=statistics&id=" + adrianas.id +"&key=" + key).read()
    adrianas.views.current = json.loads(data)["items"][0]["statistics"]["viewCount"]
    adrianas.videos = json.loads(data)["items"][0]["statistics"]["videoCount"]
    #this gets the number of total views and videos

    adrianas.views.current = int(adrianas.views.current)
    adrianas.videos = int(adrianas.videos)
    adrianas.views.average = adrianas.views.current/adrianas.videos * 1.0 
    #uses the previous information to find the average ammount of views per video

def Scan():
    getThemSubs()
    getThemViews()
    #this just calls the 2 methods

def DebugPrints():
    print("current subs: "      + str(adrianas.subs.current))
    print("original subs: "     + str(adrianas.subs.original))
    print("increase in subs: "  + str(adrianas.subs.increase))

    print("current views: "     + str(adrianas.views.current))
    print("original views: "    + str(adrianas.views.original))
    print("increase in views: " + str(adrianas.views.increase))
    #prints information to help me debug in the future

Scan()
#gets the number of subscribers & views


#Initial print
print("Adrianita has " + "{:,d}".format(int(adrianas.subs.current)) + " subscribers!")
print("Adrianita has " + "{:,d}".format(int(adrianas.views.current)) + " total views!")
print("Adrianita has an average of " + str(adrianas.views.average) + " views per video")
#prints what was found in the initial scan


# give the original counts
adrianas.subs.original  = adrianas.subs.current
adrianas.views.original = adrianas.views.current


while (1==1):
    if(time.time() > loopBrakes):
        
        print("-----")
        Scan()

        adrianas.subs.increase  = int(adrianas.subs.current)  - int(adrianas.subs.original)
        adrianas.views.increase = int(adrianas.views.current) - int(adrianas.views.original)

        DebugPrints()

        if(adrianas.subs.increase > 0):
            print("NEW SUBSCRIBER!")
            if(adrianas.subs.increase < adrianas.subs.goal):
                subsBrightness = (adrianas.subs.increase/adrianas.subs.goal) * 100
                print("Subs light at " + str(subsBrightness) + " % brightness" )
                #This determines how bright the light will be
    
        if(adrianas.views.increase > 0):
            print("NEW VIEW!")
            if(adrianas.views.increase < adrianas.views.goal):
                viewsBrightness = (adrianas.views.increase/adrianas.views.goal) * 100
                print("Views light at " + str(viewsBrightness) + " % brightness" )
                #This determines how bright the light will be
            
        if(1 == 2): #change to if the button is pressed
            adrianas.subs.original = adrianas.subs.current
            adrianas.views.original = adrianas.views.current

        loopBrakes = time.time() + scanFrequency #makes the loop happen x seconds later
