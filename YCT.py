import urllib.request
import json

key = "AIzaSyD9xf4yeziXrBDuNgSimq9XarHmVvmHDgs"
#Hard coded url: https://www.googleapis.com/youtube/v3/channels?part=statistics&id=UCT5_uqXPSVUaL5r2ChcBVeg&key=AIzaSyD9xf4yeziXrBDuNgSimq9XarHmVvmHDgs

class channel:
    def __init__(self, name, id, videoCount):
        self.name   = name
        self.id     = id
        self.videos = videoCount
        self.subs   = self.subCount(0,0)
        self.views  = self.viewCount(0,0)

    class subCount:
        def __init__(self, current, original):
            self.current  = current
            self.original = original
            self.increase = current - original

    class viewCount:
        def __init__(self, current, original):
            self.current  = current
            self.original = original 
            self.increase = current - original
            

adrianas = channel("Adrianita's channel", "UCT5_uqXPSVUaL5r2ChcBVeg", 1)


def getThemSubs():
    data = urllib.request.urlopen("https://www.googleapis.com/youtube/v3/channels?part=statistics&id=" + adrianas.id +"&key=" + key).read()
    adrianas.subs.current = json.loads(data)["items"][0]["statistics"]["subscriberCount"]

def getThemViews():
    data = urllib.request.urlopen("https://www.googleapis.com/youtube/v3/channels?part=statistics&id=" + adrianas.id +"&key=" + key).read()
    adrianas.views.current = json.loads(data)["items"][0]["statistics"]["viewCount"]
    adrianas.videos = json.loads(data)["items"][0]["statistics"]["videoCount"]
 
getThemSubs()
getThemViews()

print("AA " + str(adrianas.videos))
print("AA " + float(adrianas.views.current/adrianas.videos))

#Initial print
print("Adrianita has " + "{:,d}".format(int(adrianas.subs.current)) + " subscribers!")
print("Adrianita has " + "{:,d}".format(int(adrianas.views.current)) + " total views!")
print("Adrianita has an average of " + "{:,d}".format(int(adrianas.views.average)) + " views per video")


# give the original counts
adrianas.subs.original  = adrianas.subs.current
adrianas.views.original = adrianas.views.current


while(1==1):
    
    if(adrianas.subs.increase > 1):
        print("NEW SUBSCRIBER!")
        adrianas.subs.original = adrianas.subs.current
    
    if(adrianas.views.increase > 1):
        print("NEW VIEW!")
        adrianas.views.original = adrianas.views.current


#make a function that calculates the amount of actual subscribers/views minues the ogSubs/ogViews 
# the answer to this could determine how bright the LED light will be
# Then you push a button and the lights go back to 0 brightness
#this way, you could wake up or go to work/school and when you come back you...
#... can see how many views/subs you got while you were gone. The button will reset the brightness

    
    
    





