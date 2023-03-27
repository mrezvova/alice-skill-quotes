from random import choice

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
QUOTE_START_TEXTS = ['Ещё одна клевая цитата!:',
                     'Этот афоризм тебе точно понравится!:', 'А вот и цитата!:']
EXIT_TEXTS = ['До свидания! Афоризмизатор был рад служить',
              'Приятно было иметь дело с тобой!\n\nТвой Афоризмизатор ', 'До новых цитат! Пока!']


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

    if 'выход' in command or 'рота' in command or 'ротазимзирофа' in command:
        rand = choice(EXIT_TEXTS)
        response_text, response_tts = rand, rand
        end_session = True

    elif 'афоризмизатор' in command or 'цитата' in command or 'афоризм' in command or 'цитату' in command or 'ещё' in command and 'день' not in command and 'предсказание' not in command:
        quote, author = random_quote()
        rand_start_text = choice(QUOTE_START_TEXTS)
        text = rand_start_text
        response_text = f'{text}\n\n{quote}\n\n{author}'
        response_tts = f'{text}\n\n{quote}\n\t\t\t sil <[2000]> {author}'

    elif '' == command:
        response_text = HELLO_TEXT
        response_tts = HELLO_TEXT

    elif 'помощь' in command:
        response_text = f'Надоели цитаты? Скажи "Выход"'
        response_tts = f'Надоели цитаты? Скажи "Выход"'

    elif 'умеешь' in command:
        response_text = f'Я, Афоризмизатор могу многое! Хочешь цитату? Скажи "цитата"'
        response_tts = f'Я, Афоризмизатор могу многое! Хочешь цитату? Скажи "цитата"'

    elif 'дня' in command or 'день' in command or 'предсказание' in command:
        quote, author = random_quote()
        response_text = f'Твое предсказание на день:\n\n{quote}\n\n{author}'
        response_tts = f'Твое предсказание на день:\n\n{quote}\n\t\t\t sil <[2000]> {author}'

    else:
        response_text = 'Афоризмизатор не понял. Повтори.'
        response_tts = 'Афоризмизатор не понял. sil <[1000]> Повтори.'

    response = {
        'response': {
            'text': response_text if len(response_text) < 1024 else respond(),
            'tts': response_tts if response_tts else response_text,
            'end_session ': end_session
        },

        'version': '1.0'
    }
    return response
