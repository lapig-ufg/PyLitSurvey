from datetime import datetime
from multiprocessing import Pool




from pyalex import Works
from pymongo import MongoClient


from PyLitSurvey.config import logger, select, settings
from PyLitSurvey.model import Status


def save_db_file(openalex):
    _id = openalex['id'].split('/')[-1]
    openalex['abstract'] = openalex['abstract']
    openalex['abstract_inverted_index'] = ''
    document = {
            '_id': _id,
            **openalex,
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
    

for year in range(1900,2024):
    w = (
        Works()
        .search(
            settings.QUERY
        )
        .select(select)
        .filter(publication_year=year)
        
    )
    total = w.count()
    logger.info(f'Obtenado ano {year} total de artigos {total}')
    w = w.paginate(per_page=200, n_max=None) 
    logger.debug('init pool')
    with Pool(settings.CORES) as works:
        result_final = works.map(run_objs, w)