from ast import literal_eval
from modules.ini_config import config
from TwitterSearch import *
import datetime

# Variáveis diversas
friends = literal_eval(config['DATABASE']['friends_list'])
keywords = literal_eval(config['DATABASE']['palavras'])
nft_wallet = config['APP']['nft_wallet']
nft_wallet_wax = config['APP']['nft_wallet_wax']
nft_wallet_sol = config['APP']['nft_wallet_sol']
twitter_login = config['TWITTER']['twitter_login']
followings = []
twitters = {}
counts = 0

# Limita a busca de postagens para os últimos 4 dias  
date_now = datetime.date.today()
four_days_ago = date_now - datetime.timedelta(days=4)

# Variáveis do TwitterSearch buscando no arquivo config.ini
ts = TwitterSearch(
    # API keyws that yous saved earlier
    consumer_key = config['TWITTER']['consumer_key'],
    consumer_secret = config['TWITTER']['consumer_secret'],
    access_token = config['TWITTER']['access_token'],
    access_token_secret = config['TWITTER']['access_token_secret']
    )

# Config de busca de postagens 
tso = TwitterSearchOrder()
tso.set_keywords(keywords, or_operator=True) #'PolygonNFT', 'FreeNFT','NFTGiveaway', 'NFTGiveaways', 'NFTdrop', 'NFTcollections', 'nftcollector', 'NFTdrop'    '-filter:retweets'  '-filter:replies'
# tso.add_keyword(literal_eval(config['DATABASE']['headtags']))
# tso.set_language('en')
tso.set_since(four_days_ago)
tso.set_include_entities(False)
tso.set_result_type('recent')
tso.set_count(100)

def response_twitters_index():
    try:
        for i, twitt in enumerate(ts.search_tweets_iterable(tso)):
            # print('created_at:', twitt['created_at'], 'User_id:', twitt['id_str'], 'Tweet:', twitt['text'])
            try:
                if len(twitt['retweeted_status'].values()) > 0:
                    twitters[i] = {
                    'created_at': twitt['retweeted_status']['created_at'],
                    'Id_post': twitt['retweeted_status']['id_str'],
                    'Tweet':  twitt['retweeted_status']['text'],
                    'Id_user': twitt['retweeted_status']['user']['id_str'],
                    'followers_count': twitt['retweeted_status']['user']['followers_count'],
                    'User_post': twitt['retweeted_status']['user']['screen_name'],
                    'Url_post': f"https://twitter.com/{twitt['retweeted_status']['user']['screen_name']}/status/{twitt['retweeted_status']['id_str']}"
                    }
            except:    
                twitters[i] = {
                'created_at': twitt['created_at'],
                'Id_post': twitt['id_str'],
                'Tweet':  twitt['text'],
                'Id_user': twitt['user']['id_str'],
                'followers_count': twitt['user']['followers_count'],
                'User_post': twitt['user']['screen_name'],
                'Url_post': f"https://twitter.com/{twitt['user']['screen_name']}/status/{twitt['id_str']}"
                }
    except TwitterSearchException as exception:
            print(exception)
            print(exception.response.content)
 
    return twitters