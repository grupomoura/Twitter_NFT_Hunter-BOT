# from modules.telegrambots import telegram_msg
from lib2to3.pgen2.driver import Driver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from modules.db import insert_db, consult_db, consult_db_twitter_id, del_dbdata_7antes
# from modules.telegrambots import telegram_msg, telegram_img
from modules.ini_config import config
from modules.loading import Loader
from django.db.utils import IntegrityError
from selenium import webdriver
from ast import literal_eval
from TwitterSearch import *
from tkinter import END
import sqlite3
import pandas as pd 
import selenium
import datetime
import shutil
import numpy
import time
import os
import logging

from modules.twitter_api_busca import response_twitters_index
from modules.twitter_api_timeline import response_home_timeline

# Selenium argumentos
dir_path = os.getcwd()
profile = os.path.join(dir_path, "profile", "wpp")
options = Options()
#options.add_argument('headless')
options.add_argument('--disable-infobars')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument("disable-infobars")
options.add_argument("disable-gpu")
options.add_argument("log-level=3")
options.add_argument(r"user-data-dir={}".format(profile))
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

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

logo_img = """\n\n                                                                                                    
             .,,,             ,,,,,,.      ,,,,,,,,,,,,,,,,,,,*     ,,,,,,,,,,,,,,,,,,,,,,.         
           @@@@@@@@           @@@@@@*   @@@@@@@@@@@@@@@@@@@@@@@  *@@@@@@@@@@@@@@@@@@@@@@@@/         
          .@@@@@@@@@          @@@@@@*   @@@@@@@@@@@@@@@@@@@@@@@  %@@@@@@@@@@@@@@@@@@@@@@@@/         
          .@@@@@@@@@@@        @@@@@@*   @@@@@@                             @@@@@@                   
          .@@@@@@@@@@@@       @@@@@@*   @@@@@@                             @@@@@@                   
          .@@@@@@ /@@@@@@     @@@@@@*   @@@@@@@@@@@@@@@@@@(                @@@@@@                   
          .@@@@@@   @@@@@@    @@@@@@*   @@@@@@@@@@@@@@@@@@.                @@@@@@                   
          .@@@@@@    (@@@@@@  @@@@@@*   @@@@@@((((((((((                   @@@@@@                   
          .@@@@@@      @@@@@@ @@@@@@*   @@@@@@                             @@@@@@                   
          .@@@@@@       (@@@@@@@@@@@*   @@@@@@                             @@@@@@                   
          .@@@@@@         @@@@@@@@@@*   @@@@@@                             @@@@@@                   
          .@@@@@@          %@@@@@@@@*   @@@@@@                             @@@@@@                   
          .@@@@@@            @@@@@@@*   @@@@@@                             @@@@@@                   
                                                                                                    
          @@@@    (@@@ #@@@    @@@( @@@@@   (@@@ (@@@@@@@@@@@ #@@@@@@@@@@ @@@@@@@@@@@               
          &@@@    (@@@ #@@@    @@@( @@@@@@/ (@@@     %@@@     %@@@        @@@@    @@@&              
          &@@@@@@@@@@@ #@@@    @@@( @@@#@@@@(@@@     %@@@     %@@@@@@@@   @@@@@@@@@@.               
          &@@@    (@@@ /@@@    @@@* @@@# .@@@@@@     %@@@     %@@@        @@@&   *@@@               
          &@@@    (@@@  %@@@@@@@@%  @@@#   @@@@@     %@@@     %@@@@@@@@@@ @@@@    @@@               
                                                                                                    \n\n"""


def loading(texto_inicial='Loading...', texto_final='Next..', times=0.25):
    # loader = Loader(texto_inicial, texto_final, 0.05).start()
    with Loader(texto_inicial, texto_final, 0.05):
        for i in range(10):
            time.sleep(times/10)


def delete_cache_driver():
    Cache = r"profile\wpp\Default\Cache"
    Code_Cache = r"profile\wpp\Default\Code Cache"
    try:
        shutil.rmtree(Cache)
        shutil.rmtree(Code_Cache)
    except OSError as e:
        print(e)
    else:
        print("Cache chrome liberado com successo")


def selectRandom(names, num=5):
  return numpy.random.choice(names, num, False)


def insert_db_teste(twitt):
    if consult_db_twitter_id(twitt["Id_post"]):
        return False
    try:
        insert_db(twitt["Tweet"], twitt["User_post"], twitt["Id_post"])
    except sqlite3.IntegrityError as e:                             
        print('Twitter cancelado, encontrado no banco de dados!') 
        return False 
    except IndexError:
        try:
            insert_db(twitt['Tweet'].split(':')[0].split('http')[0].strip())
        except sqlite3.IntegrityError as e:
            print('Twitter cancelado, encontrado no banco de dados!') 
            return False
    return True


def twitters_tratamento():
    twitt_confirm = []
    twitt_reject = []

    loader = Loader('Buscando twitters_index posts..', 'Busca twitters_index finalizada!', 0.05).start()
    twitters_index = response_twitters_index()
    loader.stop()

    print(f'twitters_index: {len(twitters_index)}\n')
    logging.info(f'twitters_index: {len(twitters_index)}')

    loader = Loader('Buscando twitters_home_timeline posts..', 'Busca twitters_home_timeline finalizada!', 0.05).start()
    twitters_home_timeline = response_home_timeline()
    loader.stop()

    print(f'twitters_home_timeline: {len(twitters_home_timeline)}')
    logging.info(f'twitters_home_timeline: {len(twitters_home_timeline)}')
    
    twitters = list(twitters_home_timeline.values()) + list(twitters_index.values())
    
    print(f'\n{len(twitters)} links indexados!\n')
    logging.info(f'{len(twitters)} links indexados!')

    print('#'*80)

    for twitt in twitters:
        if 'free mint' in twitt['Tweet'].lower() or 'freemint' in twitt['Tweet'].lower():
            logging.info(f"Free mint em: {twitt['Url_post']}")
            with open("free_mint.txt", "w") as save:
                save.write(f"Free mint em: {twitt['Url_post']}\n")
        elif 'wallet' in twitt['Tweet'].lower() or 'address' in twitt['Tweet'].lower() and not 'congrats' in twitt['Tweet'].lower():
            if twitt not in twitt_confirm:
                insert = insert_db_teste(twitt)
                if insert and 'giv' in twitt['Tweet'].lower() or 'drop' in twitt['Tweet'].lower():
                    twitt_confirm.append(twitt)
        else:
            twitt_reject.append(twitt)
        
    if len(twitt_confirm):
        print(f'\n{len(twitt_confirm)} twitters selecionados!\n')
        logging.info(f'{len(twitt_confirm)} twitters selecionados!')

        return twitt_confirm
    else:
        print('\nNenhuma postagem em potencial no momento\nAguardando nova consulta..')


def follow_user(author):
    # try:
    #     insert_db_follow(author)
    # except sqlite3.IntegrityError as e:
    #     #print("Error: {}".format(e))           
    #     print('Já segue esse contato! Encontrado no banco de dados!')  
    # else:

    #Seguir usuário:
    try:
        ActionChains(driver).send_keys(Keys.HOME).perform()
        time.sleep(2)
        menu_twitter = driver.find_element(by=By.XPATH, value=('//*[@aria-label="Mais"]'))
        menu_twitter.click()
        time.sleep(2)
        menu_item_text = driver.find_elements(by=By.XPATH, value=('//*[@role="menuitem"]'))[0].text 
        if 'Deixar' in menu_item_text:
            print('Já segue esse contato! Encontrado no banco de dados!')  
            return
        driver.refresh()
        time.sleep(5)
        menu_twitter = driver.find_element(by=By.XPATH, value=('//*[@aria-label="Mais"]'))
        menu_twitter.click()
        time.sleep(2)
        ActionChains(driver).send_keys(Keys.ENTER).perform()
    except:
        pass


def retwitt():
    try:
        retwitted = driver.find_element(by=By.XPATH, value=('//*[@aria-label="Retweetado"]')) 
        if retwitted:
            logging.info('Encontrado Twitter ja retwittado!')
            return
    except:
        button_retwitt = driver.find_element(by=By.XPATH, value=('//*[@data-testid="retweet"]')) #Retwitt
        button_retwitt.click()
        time.sleep(2)
        #driver.find_element(by=By.XPATH, value=('//*[@data-testid="retweetConfirm"]')).click() #Retwitt confirma
        ActionChains(driver).send_keys(Keys.ENTER).perform()
        time.sleep(2)


def confirm_button():
    ActionChains(driver).send_keys(Keys.ARROW_DOWN).perform()
    ActionChains(driver).send_keys(Keys.ARROW_DOWN).perform()
    ActionChains(driver).send_keys(Keys.ARROW_DOWN).perform()
    time.sleep(2)
    try:
        try:
            driver.find_element(by=By.XPATH, value=('//*[@data-testid="tweetButtonInline"]')).click() # Confirmar Twitte
            logging.info('Confirmado no primeiro button!')
        except:
            ActionChains(driver).send_keys(Keys.ARROW_DOWN).perform()
            ActionChains(driver).send_keys(Keys.ARROW_DOWN).perform()
            ActionChains(driver).send_keys(Keys.ARROW_DOWN).perform() 
            time.sleep(2)
            driver.find_element(by=By.XPATH, value=('//*[@aria-label="Responder"]')).click()
            logging.info('Confirmado no segundo button!')
    except:
        logging.warning('Erro ao tentar confirmar a postagem!')
        pass


def confere_comment():
    reply_twitter = driver.find_elements(by=By.XPATH, value=('//*[@data-testid="tweet"]'))
    for reply in reply_twitter:
        if twitter_login.lower() in reply.accessible_name.lower() or twitter_login.lower() in reply.text.lower():
            return True
    return False
    

def comment(random_friends, text_twitter, url):
    ActionChains(driver).send_keys(Keys.ARROW_DOWN).perform()
    ActionChains(driver).send_keys(Keys.ARROW_DOWN).perform()
    ActionChains(driver).send_keys(Keys.ARROW_DOWN).perform()
    if confere_comment():
        print('Postagem já foi comentada!')
        return
    text_box = driver.find_element(by=By.XPATH, value=('//*[@class="public-DraftStyleDefault-block public-DraftStyleDefault-ltr"]'))
    time.sleep(1)
    text_box.click()
    if 'tag' in text_twitter.lower():
        for friend in random_friends:
            time.sleep(1)
            text_box.send_keys(f'{friend}, ')

    if 'eth' in text_twitter.lower():  
        text_box.send_keys(nft_wallet)
        # logging.info('Campanha ETH executada!')
    elif 'wax' in text_twitter.lower():  
        if nft_wallet_wax == 'none':
            logging.info('Campanha WAX perdida! Adicione uma wallet WAX!')
        else:
            text_box.send_keys(nft_wallet_wax) 
            logging.info('Campanha WAX executada!')
    elif 'solana' in text_twitter.lower() or '$sol' in text_twitter.lower():
        if nft_wallet_sol == 'none':
            logging.info('Campanha SOLANA perdida! Adicione uma wallet SOLANA!')
        else:
            text_box.send_keys(nft_wallet_sol)
            logging.info('Campanha SOLANA executada!')
    else:
        text_box.send_keys(nft_wallet)
        logging.info('Campanha ETH executada!')

    confirm_button()


def like():
    try:
        liked = driver.find_element(by=By.XPATH, value=('//*[@data-testid="unlike"]'))
        if liked:
            logging.info('Encontrado Twitter ja curtido!')
            return
    except:
        like = driver.find_element(by=By.XPATH, value=('//*[@aria-label="Curtir"]')) #Like
        if not like:
            return
        like.click()
        time.sleep(2)    


def tratar_texto():
    new_twitts = []
    twitters_db = consult_db() 
    for t in twitters_db:
        try:
            tw = t[1].split(':')[1].split('http')[0].strip()
            insert_db(tw)
        except:
            continue


def main():
    num_twitters_run = 0
    posts = 0

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s, - %(levelname)s - %(message)s', 
        filename="logger.log",
        filemode='w' # Remover para armazenar logs
        )

    print(logo_img)

    loading('Iniciando o processo..', 'Processo iniciado!', times=5)

    # Atualizando banco de dados..
    del_dbdata_7antes()

    while True:
        twitt_confirm = twitters_tratamento()
        if twitt_confirm:
            for i, twitt in enumerate(twitt_confirm):
                print('#'*80)
                text_twitter = twitt['Tweet']
       
                random_friends = selectRandom(friends)
                url = twitt['Url_post']
                driver.get(twitt['Url_post'])
                loading(f'Acessando link {i+1}: {url}',url, times=5)
                try:
                    like()    
                    retwitt() 
                    comment(random_friends, text_twitter, twitt['Url_post'])
                    time.sleep(2)
                    follow_user(twitt['User_post'])    
                    posts += 1
                    print(f'{posts} executada(s) com sucesso!\n')
                    logging.info(f'{posts} campanha(s) executada(s) com sucesso!')
                    if i+1 < len(twitt_confirm):
                        loading('Aguardando próxima postagem..', 'Iniciando nova postagem..', times=300) # 300
                except:
                    time.sleep(30)
            loading('Aguardando nova consulta..', 'Iniciando nova consulta..', times=1200)
            delete_cache_driver()


main()

# button_retwitt = driver.find_elements(by=By.XPATH, value=('//*[@data-testid="retweet"]')) 
# posts_index = driver.find_elements(by=By.XPATH, value=('//*[@data-testid="retweetConfirm"]')) 
# button_like = driver.find_elements(by=By.XPATH, value=('//*[@aria-label="Curtir"]')) 
# posts_index = driver.find_elements(by=By.XPATH, value=('//*[@data-testid="tweetButtonInline"]')) 

"""
@alanz1k 
@Punk278 
@PatrickNJ16
@bluenft
@RaffaXdy
@Bruninho0721
@Robson25404655
@Daniel69248750
@letsboracrypto
@Oriebir_1234
@gicabrother
@Raphael_RT5
@deiltonFM
@emer_jenb9
"""

# 0x5565CD8a2ea7dc42427Ba99F6b261D2985005CcB
# driver.find_element(by=By.XPATH, value=('//*[@aria-label="Responder"]')).click()

#pyinstaller --onefile main.py