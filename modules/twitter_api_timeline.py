from itertools import count
from modules.ini_config import config
from ast import literal_eval
import tweepy

# API keyws that yous saved earlier
consumer_key = config['TWITTER']['consumer_key'],
consumer_secret = config['TWITTER']['consumer_secret'],
access_token = config['TWITTER']['access_token'],
access_token_secret = config['TWITTER']['access_token_secret']

twitter_login = config['TWITTER']['twitter_login']

# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key[0], consumer_secret[0])
auth.set_access_token(access_token[0], access_token_secret)

# Creation of the actual interface, using authentication
api = tweepy.API(auth)

twitters = {}

def response_home_timeline():
    try:
        for i, twitt in enumerate(tweepy.Cursor(api.home_timeline, screen_name=f'@{twitter_login}', tweet_mode="extended").items(50)):
            try:
                if twitt.retweeted_status.author.screen_name.lower():
                    if not twitter_login.lower() in twitt.retweeted_status.author.screen_name.lower():
                        twitters[i] = {
                            'created_at': twitt.retweeted_status.created_at,
                            'Id_post': twitt.retweeted_status.id_str,
                            'Tweet':  twitt.retweeted_status.full_text,
                            'Id_user': twitt.retweeted_status.author.id_str,
                            'User_post': twitt.retweeted_status.author.screen_name,
                            'Url_post': f"https://twitter.com/{twitt.retweeted_status.author.screen_name}/status/{twitt.retweeted_status.id_str}"
                            }
            except:
                if not twitter_login.lower() in twitt.author.screen_name.lower():
                    twitters[i] = {
                        'created_at': twitt.created_at,
                        'Id_post': twitt.id_str,
                        'Tweet':  twitt.full_text,
                        'Id_user': twitt.author.id_str,
                        'User_post': twitt.author.screen_name,
                        'Url_post': f"https://twitter.com/{twitt.author.screen_name}/status/{twitt.id_str}"
                    }
    except tweepy.TweepyException as error:
        print(error)
    except:
        pass
            
    return twitters

if __name__ == "__main__":
    response_home_timeline()
    print('Fim da pesquisa')
