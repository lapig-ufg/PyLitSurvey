import re
from collections import Counter
from datetime import datetime
from multiprocessing import Pool
from pathlib import Path

from typing import Tuple

import textract
from nltk.probability import FreqDist
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.util import ngrams
from pymongo import MongoClient
from requests import get
from minio import Minio

from PyLitSurvey.config import logger, settings, stop_words
from PyLitSurvey.db import file_name_minio, save_file
from PyLitSurvey.funcs import count_keys, is_pdf, remove_path, there_words
from PyLitSurvey.model import Status

from typing import NamedTuple


import urllib3

class StatusReturn(NamedTuple):
    status: str
    mensagem: str
    url: str




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





def get_text(openalex) -> Tuple[Status, str, str]:
    doi = openalex['doi']

    _id = openalex['_id']
    logger.info(f'Downloading {_id}')
    url = openalex['doi']
    root = Path('bio_open')
    root.mkdir(exist_ok=True)
    path = root / Path(_id)
    path.mkdir(exist_ok=True)

    pdf_name = str(path / f'{_id}.pdf')
    text_name = str(path / f'{_id}.txt')
    text = ''
    http = urllib3.PoolManager()
    if not is_pdf(pdf_name):
        try:
            logger.info(pdf_name)
            if openalex['open_access']['oa_url']:
                url = openalex['open_access']['oa_url']
            
            elif openalex['primary_location']['pdf_url']:
                url = openalex['primary_location']['pdf_url']
            else:
                remove_path(path)
                return Status.NOTOPENACCESS, f'not open access {_id} {doi}', url
        except Exception as error:
            remove_path(path)
            logger.exception(error)
            return Status.ERROR, str(error), url
        try:
            response = http.request('GET', url,  timeout=3000)
        except Exception as error:
            remove_path(path)
            logger.exception(error)
            return Status.HTTPERROR, str(error), url

        if response.status == 200:
            with open(pdf_name, 'wb') as f:
                f.write(response.data)
        else:
            remove_path(path)
            logger.exception(f'not acess {response.status}')
            return Status.NOT200CODE, str(response.status), url

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
            logger.exception(f'not pdf {_id} {doi}')
            return Status.NOTPDF, f'not pdf {_id} {doi}', url

    except Exception as error:
        remove_path(path)
        logger.exception(f'error {_id} {error} {doi}')
        return Status.ERROR, str(error), url

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
        
        save_file(pdf_name)
        save_file(text_name)
        openalex['download'] = True
        openalex['lapig'] = {
                **openalex['lapig'],
                'docs': {
                    'pdf': f'{settings.MINIO_URL}/{settings.MINIO_BUCKET_NAME}/{file_name_minio(pdf_name)}',
                    'txt': f'{settings.MINIO_URL}/{settings.MINIO_BUCKET_NAME}/{file_name_minio(text_name)}',
                },
                'text':{
                    'count': count,
                    'common_words': common_words,
                    'bigramas': top_10_bigramas,
                    'trigramas': top_10_trigramas,
                    'sentences': [s for s in sentences if there_words(s)],
                    
                }
        }

        with MongoClient(settings.MONGO_URI) as client:
            db = client['biblimetry']
            colecao = db[f'pasture_open_download_v{settings.VERSION}']

            colecao.update_one(
                {'_id': _id}, {'$set': openalex}, upsert=True
            )

            logger.success(f'{_id} salve')
        return Status.SUCCESS, 'success', url
        
    except Exception as error:
        remove_path(path)
        logger.exception(_id, url, error)
        return Status.ERROR, str(error), url


def run_objs(objs) -> bool:
    _id = objs['_id']
    
    with MongoClient(settings.MONGO_URI) as client:
        db = client['biblimetry']
        colecao = db[f'pasture_open_download_v{settings.VERSION}']
        status_download = db[f'pasture_open_download_staus_v{settings.VERSION}']
        result = colecao.find_one({'_id': _id})
        if not result:
            logger.info(f'baixando {_id}')
            status, msg, url = get_text(objs)
            status_download.update_one(
                 {'_id': _id}, {'$set': {
                     'status':status,
                     'msg': msg,
                     'url': url,
                     }}, upsert=True
            )
            logger.info(f'{_id} {status} {msg}')
        else:
            logger.info(f'ja baixou {_id}')
        return status
        




logger.debug('init coleta')
with MongoClient(settings.MONGO_URI) as client:
    logger.info('conectado')
    db = client['biblimetry']
    colecao = db[f'pasture_open_v{settings.VERSION}']
    
    
    
    logger.info(f'db name pasture_open_v{settings.VERSION}')
    
    objs = list(colecao.aggregate([
              {
                "$match":{
                    "$and": [
                          {
                          "$or": [


                              {
                                "lapig.count_abstract.lue": 
                                  {
                                  "$gt": 0
                                }
                              },
                              {
                                "lapig.count_abstract.light-use_efficiency":
                                  {
                                    "$gt": 0
                                  }
                              },
                              {
                                "lapig.count_abstract.light_use_efficiency":
                                  {
                                    "$gt": 0
                                  }
                              },

                            ]
                          },
                            { "language": { "$in": ["en", "es", "pt", "fr", None] } },
                            {"open_access.is_oa":True},
                            {"download":False}
                        ]}
                            
                    
              }]))
    
    
   
    logger.info(f'len objs: {len(objs)}')
    with Pool(settings.CORES) as works:
        results = works.map(run_objs, objs)

    logger.info(results)

