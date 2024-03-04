from pymongo import MongoClient
from pyalex import Works
from pymongo.errors import DuplicateKeyError
from tqdm import tqdm
from PyLitSurvey.config import logger, settings

w = Works().search(settings.QUERY).filter(language=settings.FILTER_LANG, publication_year:settings.MAXYEAR)

total_iterations = w.count()

ITER_PER_STEP = 200

logger.info(f'Total de documentos: {total_iterations}')

with tqdm(total=total_iterations) as pbar:
    with MongoClient(settings.MONGO_URI) as client:
        db = client[f'biblimetry_{settings.VERSION}']
        colecao = db['works']
        for docs in w.paginate(per_page=ITER_PER_STEP, n_max=None):
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
            pbar.update(200)
