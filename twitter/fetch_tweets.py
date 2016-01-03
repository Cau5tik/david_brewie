import json
import tweepy

APP_SECRETS='application_secrets.json'

def writeDebug(message):
    log_file=open('log.txt','a+')
    log_file.write("Debug: %s\n" % message)
    log_file.close()

class twitterStreamListener(tweepy.StreamListener):
    def on_connect(self):
        writeDebug('Connected to twitter stream')

#The good bits:
#  Author = status.author.name
#  Status text = status.text

    def on_status(self, status):
        process_tweet(status)
        return False
        
    def on_disconnect(self):
        writeDebug('Disconnected from twitter stream')

    def on_error(self, status_code):
        if status_code == 420:
            writeDebug('error 420 received')
            exit('Error 420 received. closing.')
        else:
            writeDebug("Error received: %i" % status_code)
    
    def on_exception(self, exception):
        writeDebug("Exception: %s" % exception)

    def on_timeout(self):
        writeDebug("timeout encountered. Should probably reconnect here")
        exit()

    def on_warning(self, notice):
        writeDebug("Warning notice: %s" % notice)  


def connect_to_twitter(secrets_file):
    keys=json.load(secrets_file)
    auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
    auth.set_access_token(keys['access_token'], keys['access_secret'])

    return tweepy.API(auth)

def conect_to_queue(secrets_file):
    return True

def get_friends(twitter_api):
    friend_ids=[]
    for friend in twitter_api.me().friends():
        friend_ids.append(friend.id_str)
    return friend_ids

writeDebug('Connecting to twitter...')
try:
    twitter_api = connect_to_twitter(open(APP_SECRETS))
    writeDebug('Connected to twitter')
except Exception, e:
    message =("Could not connect to Twitter API: %s" % e)
    writeDebug(message)
    exit(message)

writeDebug('Fetching friend IDs...')
try:
    friend_ids=get_friends(twitter_api)
    writeDebug("Got friends: %s" % friend_ids)
except Exception, e:
    message=("Could not fetch list of twitter friend ids: %s" % e)
    writeDebug(message)
    exit(message)
    

myStreamListener = twitterStreamListener()
myStream = tweepy.Stream(auth=twitter_api.auth, listener=myStreamListener)

writeDebug("Connecting to tweet stream....")
try:
    myStream.filter(follow=friend_ids,languages=['en'])
except KeyboardInterrupt, e:
    writeDebug("Interrupted by keyboard")
    print('Disconnected.')

