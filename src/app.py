from flask import Flask, request
import requests

app = Flask(__name__)

HELLO_TEXT = '''
Привет!
Я Афоризмизатор.
Могу рассказать крутую цитату, если ты скажешь:
"Цитата" 
или 
"Афоризмизатор".
Захочешь выйти, скажи:
"Выход"
или
"Ротазимзирофа".
'''


def random_quote():
    response = requests.get(
        'https://quotes15.p.rapidapi.com/quotes/random/?language_code=ru', headers={"x-rapidapi-key": "4989fbb212msh00333aef0d189e4p16f2c4jsneeb2a01359ce"})
    data = response.json()
    quote, author = data['content'], data['originator']['name']
    print(f"{quote}\n\t\t\t{author}")
    return quote, author


@app.route('/', methods=['POST'])
@app.route('/alice/', methods=['POST'])
def respond():
    data = request.json
    command = data.get('request', {}).get('command', '')

    end_session = False
    response_tts = None
    response_text = None

    if 'выход' in command or 'Ротазимзирофа' in command:
        response_text = 'До свидания! Афоризмизатор был рад служить.'
        end_session = True

    elif 'цитата' in command or 'афоризмизатор' in command:
        quote, author = random_quote()
        response_text = f'{quote}\n\t\t\t{author}'
        response_tts = f'{quote}\n\t\t\t sil <[2000]> {author}'
    else:
        response_text = 'Афоризмизатор не понял. Повтори.'
        response_tts = 'Афоризмизатор не понял. sil <[1000]> Повтори.'

    response = {
        'response': {
            'text': response_text,
            'tts': response_tts if response_tts else response_text,
            'end_session ': end_session
        },

        'version': '1.0'
    }
    return response
