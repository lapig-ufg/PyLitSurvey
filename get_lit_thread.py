from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from pyalex import Works
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from PyLitSurvey.config import logger, settings
import requests

def process_documents(docs, db):
    colecao = db['works']
    new_docs = []
    for doc in docs:
        _id = doc.pop('id')
        doc['_id'] = _id
        new_docs.append(doc)
    try:
        colecao.insert_many(new_docs)
    except Exception as e:
        for doc in new_docs:
            try:
                colecao.insert_one(doc)
            except DuplicateKeyError:
                logger.info(f'ja existe {doc["_id"]}')
            except Exception as e:
                logger.exception(e)

def save_failed_parameters(params, db):
    fails_collection = db['fails']
    fails_collection.insert_one(params)

def fetch_and_process_batch(w, db):
    try:
        for docs in w.paginate(per_page=100, n_max=None):
            process_documents(docs, db)
            time.sleep(0.6)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 503:
            params = {
                'query': settings.QUERY,
                'filter_language': settings.FILTER_LANG,
                'filter_year': settings.MAXYEAR,
                'error': str(e)
            }
            save_failed_parameters(params, db)
        else:
            logger.exception(e)
    except Exception as e:
        logger.exception(e)

def main():
    w = Works().search(settings.QUERY).filter(language=settings.FILTER_LANG, publication_year=settings.MAXYEAR)
    total_iterations = w.count()
    ITER_PER_STEP = 100
    DELAY = 0.6

    logger.info(f'Total de documentos: {total_iterations}')
    total_pages = (total_iterations + ITER_PER_STEP - 1) // ITER_PER_STEP

    with tqdm(total=total_iterations) as pbar:
        with MongoClient(settings.MONGO_URI) as client:
            db = client[f'biblimetry_{settings.VERSION}']
            with ThreadPoolExecutor(max_workers=30) as executor:
                futures = []
                for page_number in range(1, total_pages + 1, 30):
                    future = executor.submit(fetch_and_process_batch, w, db)
                    futures.append(future)
                    time.sleep(DELAY)

                for future in as_completed(futures):
                    try:
                        future.result()
                    except Exception as e:
                        logger.exception(e)
                    finally:
                        pbar.update(ITER_PER_STEP)

if __name__ == '__main__':
    main()
