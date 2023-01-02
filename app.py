from flask import Flask, request 
import requests
import config

app = Flask(__name__)

token = config.token


fr_to_en_mode = True
en_to_fr_mode = False 



def translation(mode, word):
    if mode == 'en_to_fr_mode':
        try:
            url = "https://nlp-translation.p.rapidapi.com/v1/translate"

            querystring = {"text":f"{word}","to":"fr","from":"en"}
            headers = {"X-RapidAPI-Key": "31d9d4b8d6msh56397bfe8e10815p18d5cdjsn9fac02bed69a","X-RapidAPI-Host": "nlp-translation.p.rapidapi.com"}

            response = requests.request("GET", url, headers=headers, params=querystring)
            x = response.json()['translated_text']['fr']
            return f"{x}\n--🇫🇷 --\n{word}\n--🇬🇧 --\n/commands"
        except:
            return 'Try again'

    if mode == 'fr_to_en_mode':
        try:
            url = "https://nlp-translation.p.rapidapi.com/v1/translate"

            querystring = {"text":f"{word}","to":"en","from":"fr"}
            headers = {"X-RapidAPI-Key": "31d9d4b8d6msh56397bfe8e10815p18d5cdjsn9fac02bed69a","X-RapidAPI-Host": "nlp-translation.p.rapidapi.com"}

            response = requests.request("GET", url, headers=headers, params=querystring)

            x = response.json()['translated_text']['en']
            return f"{x}\n--🇬🇧 --\n{word}\n--🇫🇷 --\n/commands"
        except:
            return 'Try again'


def send_message(chat_id, message):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    requests.post(url, data={'chat_id': chat_id, 'text': message})


def message_processing(message):
    global fr_to_en_mode
    global en_to_fr_mode
    if message == '/commands':
        return '/en_to_fr_mode - English to French mode🇬🇧\
\n/fr_to_en_mode - French to English mode🇫🇷\
\n/mode - check you current mode'
    if message == '/start':
        return "Hello!\nThis bot can help you translate!\nFrench into English\n/fr_to_en_mode 🇫🇷\n-----\nEnglish to French\n/en_to_fr_mode 🇬🇧"
    if message == '/fr_to_en_mode':
        fr_to_en_mode = True
        en_to_fr_mode = False
        return 'French into English mode is on!\nPut French word!\n🇫🇷'
    if message == '/en_to_fr_mode':
        fr_to_en_mode = False
        en_to_fr_mode = True
        return 'English into French mode is on!\nPut English word!\n🇬🇧'
    if fr_to_en_mode == True and en_to_fr_mode == False and message == '/mode':
        return 'French to English mode is active!\nPut English word!\n🇬🇧'
    if fr_to_en_mode == False and en_to_fr_mode == True and message == '/mode':
        return 'English to French mode is active!\nPut French word!\n🇫🇷'
    if fr_to_en_mode == True and en_to_fr_mode == False:
        return translation('fr_to_en_mode', message)
    if fr_to_en_mode == False and en_to_fr_mode == True:
        return translation('en_to_fr_mode', message)





        


@app.route("/", methods=["POST", "GET"])
def hello_world():
    if request.method == "POST":
        r = request.get_json()
        print(r)
        chat_id = r['message']['chat']['id']
        message = r['message']['text']
        send_message(chat_id, message_processing(message))
        return "<p>Webhook for telegram bot done</p>"
    if request.method == 'GET':
        return "<p>Webhook for telegram bot done</p>"



