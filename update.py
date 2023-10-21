from datetime import datetime
from multiprocessing import Pool
from random import randint
from time import sleep

from pyalex import Works
from pymongo import MongoClient
from requests import get

from PyLitSurvey.config import logger, select, settings
from PyLitSurvey.funcs import count_keys
from PyLitSurvey.model import Status

BASE_API = 'https://api.openalex.org/'


def get_id(text):
    return text.replace('https://openalex.org/', '')


def get_data(url, get_item=False, erro=1):
    try:
        response = get(url)
        match response.status_code:
            case 200:
                if get_item is False:
                    return response.json()
                else:
                    return response.json()[get_item]
            case 429:
                if erro < 5:
                    _time = randint(erro, 5 * erro)
                    logger.info(
                        f'Estou esperando por {_time} para tenta pegar os dados\n{url}'
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


def save_db_file(openalex):
    _id = openalex['id'].split('/')[-1]
    try:
        ngrams = get_data(f'{BASE_API}works/{_id}/ngrams', 'ngrams')
    except:
        ngrams = f'https://api.openalex.org/works/{_id}/ngrams'

    if not openalex['abstract_inverted_index'] is None:
        abstract = openalex['abstract']
    else:
        abstract = ''
    openalex['abstract_inverted_index'] = ''

    author_fist, source_fist = None, None

    if len(openalex['authorships']) > 0:
        try:
            author_id = get_id(openalex['authorships'][0]['author']['id'])
            author_fist = get_data(
                f'{BASE_API}authors/{author_id}?select=summary_stats'
            )
        except TypeError:
            pass

    if len(openalex['locations']) > 0:
        try:
            source_id = get_id(openalex['locations'][0]['source']['id'])
            source_fist = get_data(
                f'{BASE_API}sources/{source_id}?select=summary_stats'
            )
        except TypeError:
            pass

    document = {
        '_id': _id,
        'download': False,
        'source_fist': source_fist,
        'author_fist': author_fist,
        'lapig': {'count_abstract': count_keys(abstract)},
        **openalex,
        'ngrams': ngrams,
    }
    with MongoClient(settings.MONGO_URI) as client:
        db = client['biblimetry']
        colecao = db[f'pasture_open_v{settings.VERSION}']

        colecao.update_one(
            {'_id': document['_id']}, {'$set': document}, upsert=True
        )

        logger.success(f'{_id} salve')
        return Status.SUCCESS, 'success'


def run_objs(objs):
    logger.info('start objs')
    for obj in objs:
        with MongoClient(settings.MONGO_URI) as client:
            db = client['biblimetry']
            status_download = db[f'baixado_pasture_open_v{settings.VERSION}']
            _id = obj['id'].split('/')[-1]
            if not status_download.find_one({'_id': _id}):
                status_file = save_db_file(obj)
                status_download.update_one(
                    {'_id': _id},
                    {
                        '$set': {
                            '_id': _id,
                            'datetime': datetime.now(),
                            'status': status_file,
                        }
                    },
                    upsert=True,
                )
            else:
                logger.info(f'Ja baixou ou fez o check: {_id}')
    return True


for year in range(1900, 2024):
    w = (
        Works()
        .search(settings.QUERY)
        .select(select)
        .filter(publication_year=year)
    )
    total = w.count()
    logger.info(f'Obtenado ano {year} total de artigos {total}')
    w = w.paginate(per_page=200, n_max=None)
    logger.debug('init pool')
    with Pool(settings.CORES) as works:
        result_final = works.map(run_objs, w)
