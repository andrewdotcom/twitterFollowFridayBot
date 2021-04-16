import tweepy
import time
import random
import os

# Get the user's followers
def get_followers(api, username):
    followers = []
    try:
        api.verify_credentials()
    except:
        print("Error during authentication")
        return followers

    for page in tweepy.Cursor(api.followers, screen_name=username, wait_on_rate_limit=True,count=200).pages():
        try:
            followers.extend(page)
        except tweepy.TweepError as e:
            print("Going to sleep:", e)
            time.sleep(60)
    return followers

#Tweet the follow friday string from random followers
def tweet(api, followers, peeps=0, debug=False):
    if len(followers) == 0 or peeps == 0:
        return
    
    count = 1
    ffs = []

    while count <= peeps:
        random_index = random.randint(0,len(followers)-1)
        ffs.append(followers[random_index].screen_name)
        count += 1

    ff_string = f'#followfriday @{" @".join(ffs)}'

    try:
        if debug == False:
            api.update_status(ff_string)
        else:
            print(ff_string)
    except:
        print("Could not post")

def ff(debug=False, numberofshouts=5):
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(os.environ.get('T_KEY'), os.environ.get('T_SECRET'))
    auth.set_access_token(os.environ.get('T_TOKEN'), os.environ.get('T_TOKEN_SECRET'))
    
    api = tweepy.API(auth) 

    try:
        api.verify_credentials()
        print("Twitter authentication OK - going for it! 👍🏻")
    except:
        print("Error during Twitter authentication - barfing out 🤮")
        return

    try:
        tweet(api, get_followers(api, "andrewdotcom"), numberofshouts, debug)
    except:
        print("Abort, Abort! - Could not post to twitter 😭")
    #return

#Follow Friday - True for Debug (won't actually tweet)
ff(False, 5)