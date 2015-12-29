#!/bin/python

import tweepy
import json

try:
    appCredsFile=open('application_secrets.json','r')
except:
    template=dict()
    template['consumer_key']=""
    template['consumer_secret']=""
    appCredsFile=open('application_secrets.json','w')
    appCredsFile.write(json.dumps(template))
    appCredsFile.close()
    exit('Please place the consumer key and consumer secret in ./application_secrets.json')

try:
    keys=json.load(appCredsFile)
except:
    exit('application_secrets.json must be a valid JSON file')

appCredsFile.close()

try:
    consumer_key=keys['consumer_key']
    consumer_secret=keys['consumer_secret']
except Exception, e:
    exit("Could not parse consumer_key and consumer_secret from application_secrets.json: %s" % e)

if (consumer_key == '') or (consumer_secret == ''):
    exit('Please place the consumer key and consumer secret in ./application_secrets.json')

try:
    auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
except Exception, e:
    exit("Could not start OAuth handshake: %s" % e)

url=auth.get_authorization_url()
print('Please visit the following link and log in to twitter to verify access to your account')
print(url)
print('\n')

verified=False
while not verified:
    code=input('Verification code: ')
    try:
        token=auth.get_access_token(verifier=str(code))
        verified=True
    except Exception, e:
        print("Could not get API token: %s" % e)

keys['access_token']=token[0]
keys['access_secret']=token[1]
    
appCredsFile=open('application_secrets.json','w')
appCredsFile.write(json.dumps(keys))
appCredsFile.close()

print('done.')
