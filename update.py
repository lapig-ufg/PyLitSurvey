from datetime import datetime
from multiprocessing import Pool
from random import randint
from time import sleep

from typing import List

from pyalex import Works
from pymongo import MongoClient


from PyLitSurvey.config import logger, select, settings
from PyLitSurvey.funcs import count_keys, get_id, get_data
from PyLitSurvey.model import Status

BASE_API = 'https://api.openalex.org/'


def save_db_file(openalex:dict):
    _id = openalex['id'].split('/')[-1]
    try:
        ngrams = get_data(f'{BASE_API}works/{_id}/ngrams', 'ngrams')
    except:
        ngrams = f'https://api.openalex.org/works/{_id}/ngrams'
    title = openalex['title']
    if not openalex['abstract_inverted_index'] is None:
        abstract = f"{title} {openalex['abstract']}"
    else:
        abstract = f'{title}'
    openalex['abstract_inverted_index'] = ''

    author_first, source_first = None, None

    if len(openalex['authorships']) > 0:
        try:
            author_id = get_id(openalex['authorships'][0]['author']['id'])
            author_first = get_data(
                f'{BASE_API}authors/{author_id}'
            )
        except TypeError:
            pass

    if len(openalex['locations']) > 0:
        try:
            source_id = get_id(openalex['locations'][0]['source']['id'])
            source_first = get_data(
                f'{BASE_API}sources/{source_id}?select=summary_stats,cited_by_count,x_concepts'
            )
        except TypeError:
            pass

    publication_date = openalex['publication_date']
    openalex['publication_date'] = datetime.strptime(publication_date,'%Y-%m-%d')
    document = {
        '_id': _id,
        'download': False,
        'source_first': source_first,
        'author_first': author_first,
        'text':{'abstract':abstract},
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
        return Status.SUCCESS, Status.SUCCESS


def process_obj(obj:dict):
    try:
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
                sleep(randint(1, 2))
                logger.info(f'Ja baixou ou fez o check: {_id}')
        return True
    except:
        logger.exception(f'error in process: {obj["id"]}')
        return False



def run_objs(objs: List[dict]) -> List[bool]:
    logger.info('start objs')
    results = [False]
    with Pool(settings.CORES) as works:
        results = works.map(process_obj, objs)
    return results

for year in reversed(range(1900, 2024)):
    with MongoClient(settings.MONGO_URI) as client:
        db = client['biblimetry']
        docs_yaear = db[f'baixado_pasture_year_v{settings.VERSION}']
        status_year = docs_yaear.find_one({'_id': year})

    if not status_year:
        logger.info(f'Iniciando ano {year}')
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
        
        for objs in w:
            result_final =  run_objs(objs)
            
        if all(result_final):
            with MongoClient(settings.MONGO_URI) as client:
                db = client['biblimetry']
                docs_yaear = db[f'baixado_pasture_year_v{settings.VERSION}']
                docs_yaear.update_one(
                        {'_id': year},
                        {
                            '$set': {
                                '_id': year,
                                'datetime': datetime.now(),
                                'status': Status.SUCCESS.value,
                            }
                        },
                        upsert=True,
                    )
