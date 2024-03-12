import pandas as pd
from pymongo import MongoClient
from PyLitSurvey.funcs import to_row, abstract_inverted_index2abstract
from PyLitSurvey.config import settings




def to_csv_all_columns():
    BUCKT = 10_000
    SKIP = 0
    df_all = pd.DataFrame()
    while True:
        with MongoClient(settings.MONGO_URI) as client:
            db = client[f'biblimetry_{settings.VERSION}']
            colection = db['works']
            all_data = list(colection.find({}).limit(BUCKT).skip(SKIP))
            
            df_all = pd.concat([df_all, pd.DataFrame([to_row(doc) for doc in all_data])])
            if not all_data:
                break
            
            SKIP += BUCKT
            print(f'{SKIP}')

    df_all.to_csv('output/all_columns.csv', index=False)
    
def dict_to_row_short(doc):
    
    row =  {
        '_id': doc.get('_id',''),
        'title': doc.get('title',''),
        'doi': doc.get('doi','')
 
    }
    try:
        row['abstract'] = abstract_inverted_index2abstract(doc.get('abstract_inverted_index',{}))
    except Exception as e:
        ...
    for i, keyword in enumerate(doc.get('keywords',[])):
        row[f'keyword_{i}'] = keyword.get('keyword',' ')
        row[f'keyword_score_{i}'] = keyword.get('score',None)

    return row

def to_csv():
    BUCKT = 10_0
    SKIP = 0
    df_all = pd.DataFrame()
    while True:
        with MongoClient(settings.MONGO_URI) as client:
            db = client[f'biblimetry_{settings.VERSION}']
            colection = db['works']
            all_data = list(colection.find({},{
                '_id':1,
                'title':1,
                'doi':1,
                'keywords':1,
                'abstract_inverted_index':1
                
                
                }).limit(BUCKT).skip(SKIP))
            
            df_all = pd.concat([df_all, pd.DataFrame([dict_to_row_short(doc) for doc in all_data])])
            if not all_data:
                break
            
            SKIP += BUCKT
            print(f'{SKIP}')
            print(f'{df_all}')
    df_all.to_csv('output/all_short.csv', index=False)

to_csv()