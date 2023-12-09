import shutil
import numpy as np
from random import randint
from time import sleep
from requests import get
from nltk.tokenize import word_tokenize


from PyLitSurvey.config import logger, settings


def get_data(url:str, get_item=False, erro=1):
    """
        Get json data from url
    Args:
        url (str): url api endpoint (https://api.openalex.org/works/W1814889)
        get_item (bool, optional): json key. Defaults to False.
        erro (int, optional): Number error. Defaults to 1.

    Returns:
        _type_: _description_
    """
    try:
        response = get(url)
        match response.status_code:
            case 200:
                if get_item is False:
                    return response.json()
                else:
                    return response.json()[get_item]
            case 429:
                if erro < 30:
                    _time = randint(erro, 5 * erro)
                    logger.info(
                        f'Estou esperando por {_time} para tentar pegar os dados\n{url}'
                    )
                    sleep(_time)
                    erro += 1
                    get_data(url, get_item, erro)
                else:
                    return 429
            case _:
                logger.error(f'Error in status: {response.status_code}\n{url}')
                return response.status_code
    except:
        logger.exception('error not map')
        return dict()
    
    
    
def there_words(txt):
    for i in settings.COUNTING_WORDS:
        if i.lower() in word_tokenize(txt.lower()):
            return True
    return False

def get_id(text:str)-> str:
    """
        Get the id from the url
    Args:
        text (str): The text with the url

    Returns:
        str:  The id
    """
    return text.replace('https://openalex.org/', '')


def count_keys(text):
    words = [i.lower() for i in settings.COUNTING_WORDS if len(i.split(' ')) == 1]
    ngramas = [i.lower() for i in settings.COUNTING_WORDS if len(i.split(' ')) > 1]
    tokens = word_tokenize(text.lower())

    count = {}
    count_words_tmp = dict(
        zip(*np.unique([i for i in tokens if i in words], return_counts=True))
    )

    for i in words:
        try:
            count[i] = int(count_words_tmp[i])
        except:
            count[i] = 0

    for key in ngramas:
        id_key = key.lower().replace(' ', '_').replace('/', '_')
        count[id_key] = text.lower().count(key.lower())
    return count


def is_pdf(file_path):
    try:
        with open(file_path, 'rb') as file:
            # Leia os primeiros 5 bytes do arquivo
            header = file.read(5)
            # Verifique se a assinatura começa com "%PDF-"
            if header.startswith(b'%PDF-'):
                return True
    except:
        return False
    return False


def get_francao(valor, total, fracao):
    return (valor * fracao / total) / 100


def remove_path(path):
    if path.exists():
        logger.debug('remove path')
        shutil.rmtree(path)
