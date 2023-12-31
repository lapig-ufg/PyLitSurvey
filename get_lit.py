import random
import re
from collections import Counter
from datetime import datetime
from multiprocessing import Pool
from pathlib import Path
from time import sleep
from typing import Tuple

import textract
from nltk.probability import FreqDist
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.util import ngrams
from pyalex import Authors, Sources, Works
from pymongo import MongoClient
from requests import get

from PyLitSurvey.config import logger, select, settings, stop_words
from PyLitSurvey.db import file_name_minio, save_file
from PyLitSurvey.funcs import count_keys, get_francao, is_pdf, remove_path
from PyLitSurvey.model import Status


def get_keys(txt):
    palavras = [
        'conversion factor',
        'gpp',
        'gross primary productivity',
        'gpp measurements',
        'plant photosynthesis data',
        'primary production data',
        'ecosystem productivity',
        'carbon fixation rates',
        'vegetation productivity',
        'dry biomass',
        'photosynthetic activity',
        'npp',
        'net primary productivity',
        'npp measurements',
        'biomass accumulation',
        'ecosystem energy',
        'net carbon',
        'plant respiration',
        'lue',
        'fapar',
        'par',
        'npp/gpp ratios',
        'grazing',
        'land',
        'pastureland',
        'pastures',
        'rangelands',
        'grasslands',
        'savannas',
        'grassland',
        'ecosystems',
        'meadows',
        'prairies',
        'steppes',
        'grazable',
        'forestland',
        'shrublands',
        'gpp',
        'satellite',
        'spectral',
    ]
    for i in palavras:
        if i in txt.lower():
            return True
    return False


def get_weigth(url):
    _id_refre = url.split('/')[-1]
    try:
        w = Works()[_id_refre]

        try:
            concepts = w['concepts']
            max_concepts = len(concepts)
            concepts_interesse = len(
                [i for i in concepts if get_keys(i['display_name'])]
            )
            concepts_weigth = get_francao(concepts_interesse, max_concepts, 33)
        except:
            concepts_weigth = 0

        try:
            common_words = w['common_words']
            max_common_words = len(common_words)
            common_words_interesse = len(
                [i for i in common_words if get_keys(i[0])]
            )
            common_words_weigth = get_francao(
                common_words_interesse, max_common_words, 33
            )
        except:
            common_words_weigth = 0

        try:
            ngrams = get(w['ngrams_url']).json()['ngrams']
            totoal = len(ngrams)
            interesse = len([n for n in ngrams if get_keys(n['ngram'])])
            ngrams_weigth = get_francao(interesse, totoal, 33)
        except:
            ngrams_weigth = 0

        return (_id_refre, ngrams_weigth + concepts_weigth)
    except:
        return (_id_refre, 0)


def get_info_text(text):
    sentences = sent_tokenize(text)
    words = word_tokenize(
        text.lower()
    )  # Tokenização de palavras e conversão para minúsculas
    words_without_stopwords = [
        word for word in words if word.isalnum() and word not in stop_words
    ]

    # Frequência das palavras
    freq_dist = FreqDist(words_without_stopwords)

    # Palavras mais comuns
    common_words = freq_dist.most_common(10)

    count = count_keys(text)

    # Crie trigramas
    trigramas = list(ngrams(words_without_stopwords, 3))
    bigramas = list(ngrams(words_without_stopwords, 2))

    # Conte a frequência dos trigramas
    contagem_trigramas = Counter(trigramas)
    contagem_bigramas = Counter(bigramas)

    # Encontre os 10 trigramas mais usados
    top_10_trigramas = contagem_trigramas.most_common(10)
    top_10_bigramas = contagem_bigramas.most_common(10)
    return common_words, top_10_bigramas, top_10_trigramas, sentences, count


def get_text(openalex) -> Tuple[Status, str]:
    doi = openalex['doi']

    _id = openalex['id'].split('/')[-1]
    url = ''
    root = Path('bio_open')
    root.mkdir(exist_ok=True)
    path = root / Path(_id)
    path.mkdir(exist_ok=True)

    pdf_name = path / f'{_id}.pdf'
    text_name = path / f'{_id}.txt'
    text = ''

    if not is_pdf(pdf_name):
        try:
            logger.debug(pdf_name)
            if openalex['open_access']['oa_url']:
                url = openalex['open_access']['oa_url']
            else:
                remove_path(path)
                return Status.NOTOPENACCESS, f'not open access {_id} {doi}'
        except Exception as error:
            remove_path(path)
            logger.debug(error)
            return Status.ERROR, str(error)
        try:
            response = get(url, allow_redirects=True)
        except Exception as error:
            remove_path(path)
            logger.exception(error)
            return Status.HTTPERROR, str(error)

        if response.status_code == 200:
            with open(pdf_name, 'wb') as f:
                f.write(response.content)
        else:
            remove_path(path)
            logger.debug(f'not acess {response.status_code}')
            return Status.NOT200CODE, str(response.status_code)

    try:
        if is_pdf(pdf_name):
            text = re.sub(
                r'\s+',
                ' ',
                textract.process(pdf_name)
                .decode('utf-8')
                .replace('-\n', '')
                .replace('\n', ' '),
            )
            with open(text_name, 'w') as f:
                f.write(text)
        else:
            remove_path(path)
            logger.error(f'not pdf {_id} {doi}')
            return Status.NOTPDF, f'not pdf {_id} {doi}'

    except Exception as error:
        remove_path(path)
        logger.debug(f'error {_id} {error} {doi}')
        return Status.ERROR, str(error)

    try:
        if text == '':
            with open(text_name, 'r') as f:
                text = f.read()
        (
            common_words,
            top_10_bigramas,
            top_10_trigramas,
            sentences,
            count,
        ) = get_info_text(text)

        ### Dar peso a referencia
        referenced_works = []
        for ref in openalex['referenced_works']:
            referenced_works.append(get_weigth(ref))

        authorships = []

        for n, authorship in enumerate(openalex['authorships']):
            if n == 0:
                sleep(random.randint(5, 10))
                summary_stats = Authors()[
                    authorship['author']['id'].replace(
                        'https://openalex.org/', ''
                    )
                ]['summary_stats']
                authorship['author']['summary_stats'] = summary_stats
                authorships.append(authorship)
            if n > 0:
                break

        openalex['author_first'] = authorships

        locations = []

        for n, location in enumerate(openalex['locations']):
            if n == 0:
                sleep(random.randint(5, 10))
                summary_stats = Sources()[
                    location['source']['id'].replace(
                        'https://openalex.org/', ''
                    )
                ]['summary_stats']
                location['source']['summary_stats'] = summary_stats
                locations.append(location)
            if n > 0:
                break

        openalex['souce_first'] = locations

        openalex['referenced_works'] = referenced_works
        save_file(pdf_name)
        save_file(text_name)
        document = {
            '_id': _id,
            **openalex,
            'download': True,
            'lapig': {
                'docs': {
                    'pdf': f'{settings.MINIO_URL}/{settings.MINIO_BUCKET_NAME}/{file_name_minio(pdf_name)}',
                    'txt': f'{settings.MINIO_URL}/{settings.MINIO_BUCKET_NAME}/{file_name_minio(text_name)}',
                },
                'count': count,
                'common_words': common_words,
                'bigramas': top_10_bigramas,
                'trigramas': top_10_trigramas,
                'sentences': [s for s in sentences if get_keys(s)],
            },
        }

        with MongoClient(settings.MONGO_URI) as client:
            db = client['biblimetry']
            colecao = db[f'pasture_open_v{settings.VERSION}']

            colecao.update_one(
                {'_id': document['_id']}, {'$set': document}, upsert=True
            )

            logger.success(f'{_id} salve')
        return Status.SUCCESS, 'success'
    except Exception as error:
        remove_path(path)
        logger.exception(_id, url, error)
        return Status.ERROR, str(error)


def run_objs(objs):
    logger.info('start objs')
    for obj in objs:
        try:
            with MongoClient(settings.MONGO_URI) as client:
                db = client['biblimetry']
                status_download = db[f'baixado_pasture_open_v{settings.VERSION}']
                _id = obj['id'].split('/')[-1]
                if not status_download.find_one({'_id': _id}):
                    status_file = get_text(obj)
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
        except:
            return False
    return True


logger.debug('init coleta')


for year in reversed(range(1900, 2024)):
    logger.info(f'Year {year}')
    with MongoClient(settings.MONGO_URI) as client:
        db = client['biblimetry']
        colecao = db[f'pasture_open_year_v{settings.VERSION}']
        d = colecao.find_one({'_id':year})
    if not d:
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
        if all(result_final):
            with MongoClient(settings.MONGO_URI) as client:
                db = client['biblimetry']
                colecao = db[f'pasture_open_year_v{settings.VERSION}']
                colecao.update_one(
                    {'_id': year}, {'$set': {'_id':year,'baixado':True}}, upsert=True
                )

