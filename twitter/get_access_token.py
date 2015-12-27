#!/bin/python

import tweepy

try:
    appCredsFile=open('application_secrets','r')
except:
    appCredsFile=open('application_secrets','w')
    appCredsFile.write('consumer_key=\n')
    appCredsFile.write('consumer_secret=\n')
    appCredsFile.close()
    exit('Please place the consumer key and consumer secret in ./application_secrets')

consumer_key=''
consumer_secret=''

for line in appCredsFile.readlines():
    line=line.split('=')
    if line[0] == 'consumer_key':
        consumer_key=line[1].strip()
    if line[0] == 'consumer_secret':
        consumer_secret=line[1].strip()

appCredsFile.close()

if (consumer_key == '') or (consumer_secret == ''):
    exit('Please place the consumer key and consumer secret in ./application_secrets')

try:
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
except Exception, e:
    exit("Could not get verification link: %s" % e)

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
    
appCredsFile=open('application_secrets','a+')
appCredsFile.write("access_token=%s" % token[0])
appCredsFile.write('\n')
appCredsFile.write("access_secret=%s" % token[1])
appCredsFile.write('\n')
appCredsFile.close()

print('done.')
