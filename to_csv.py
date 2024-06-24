import pandas as pd


from pymongo import MongoClient
from PyLitSurvey.funcs import to_row, abstract_inverted_index2abstract
from PyLitSurvey.config import settings, logger

MED = pd.read_csv('med.csv')

SOUCER = []
SOUCER_ID = []

def filter_by_issn(locations):
    """
    Filters locations data based on ISSN.

    Args:
    - locations (list): List of location dictionaries.

    Returns:
    - Tuple of comma-separated strings: (display_name, souce_id, l_issns, soucer_is_med)

    Raises:
    - Exception: If there's an error processing locations data.
    """
    # [{"is_oa": false, "landing_page_url": "https://doi.org/10.1146/annurev.ecolsys.28.1.517", "pdf_url": null, "source": {"id": "https://openalex.org/S4210205963", "display_name": "Annual review of ecology and systematics", "issn_l": "0066-4162", "issn": ["0066-4162", "2330-1902"], "is_oa": false, "is_in_doaj": false, "host_organization": "https://openalex.org/P4310320373", "host_organization_name": "Annual Reviews", "host_organization_lineage": ["https://openalex.org/P4310320373"], "host_organization_lineage_names": ["Annual Reviews"], "type": "journal"}, "license": null, "version": null, "is_accepted": false, "is_published": false}]
    l_issns = []
    display_name = []  
    souce_id = []
    is_med = False
    soucer_is_med = []
    try:
        for location in locations:
            try:
                souce = location.get('source',{})
                if souce is not None:
                    local_is_med = False
                    _id = str(souce.get("id",'NAN')).replace( 'https://openalex.org/','')
                    if len(MED[MED['id'] == _id]) > 0:
                        is_med = True
                        local_is_med = True
                    name = str(souce.get("display_name",'NAN'))
                    isss = str(souce.get("issn_l",'NAN'))
                    if not _id in SOUCER_ID:
                        SOUCER_ID.append(_id)
                        SOUCER.append({
                            'id':_id,
                            'name':name,
                            'issn_l':isss
                            
                        })
                    display_name.append(name)
                    souce_id.append(_id)
                    l_issns.append(isss)
                    soucer_is_med.append(str(local_is_med))
                    
                    
            except Exception:
                logger.exception(location)
                raise Exception('Location fall')
        return ', '.join(display_name), ', '.join(souce_id), ', '.join(l_issns), ', '.join(soucer_is_med)
    except:
        logger.exception('')
        raise Exception('error')
        

def to_csv_all_columns():
    """
    Retrieves all data from MongoDB and exports all columns to a CSV file 'all_columns.csv'.
    """
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
    """
    Converts a dictionary of data into a row format for CSV export.

    Args:
    - doc (dict): Dictionary of data.

    Returns:
    - dict: Row formatted data.

    Notes:
    - Handles conversion of abstract_inverted_index to abstract.
    - Appends keywords and their scores as columns.
    """
    display_name, souce_id, l_issns, is_med = filter_by_issn(doc.get('locations',[]),)
    if True:
        
        row =  {
            '_id': doc.get('_id',''),
            'title': doc.get('title',''),
            'doi': doc.get('doi',''),
            'language':doc.get('language',''),
            'type_crossref':doc.get('type_crossref',''),
            'ismed': is_med,
            'id_sourcer': str(souce_id),
            
            'cited_by_count':doc.get('cited_by_count',0),
            'publication_date':doc.get('publication_date',None),
            'referenced_works_count':doc.get('referenced_works_count',0),
            'relevance_score':doc.get('relevance_score',0),
                
            #'issns':str(l_issns),
            'type':doc['type']
            
 
        }
        
        try:
            row['abstract'] = abstract_inverted_index2abstract(doc.get('abstract_inverted_index',{}))
        except Exception as e:
            ...
        for i, keyword in enumerate(doc.get('keywords',[])):
            row[f'keyword_{i}'] = keyword.get('keyword',' ')
            row[f'keyword_score_{i}'] = keyword.get('score',None)

        return row
    else:
        return {}

def to_csv():
    """
    Retrieves specific data from MongoDB, filters by article type and non-empty keywords,
    and exports filtered data to CSV files 'nomed_filtrado.csv' and 'soucer.csv'.
    """
    BUCKT = 10_000
    SKIP = 0
    df_all = pd.DataFrame()
    while True:
        with MongoClient(settings.MONGO_URI) as client:
            db = client[f'biblimetry_{settings.VERSION}']
            colection = db['works']
            all_data = list(colection.find({
                'type':'article',
                'keywords':{'$ne':[]}
                },{
                '_id':1,
                'title':1,
                'doi':1,
                'language':1,
                'type_crossref':1,
                'locations':1,
                'type':1,
                
                'cited_by_count':1,
                'publication_date':1,
                'referenced_works_count':1,
                'relevance_score':1,
                
                'keywords':1,
                'abstract_inverted_index':1
                
                
                }).limit(BUCKT).skip(SKIP))
            
            df_all = pd.concat([df_all, pd.DataFrame([dict_to_row_short(doc) for doc in all_data])])
            if not all_data:
                break
            
            SKIP += BUCKT
            print(f'{SKIP}')
    df_all.to_csv('output/nomed_filtrado.csv', index=False)
    pd.DataFrame(SOUCER).to_csv('output/soucer.csv', index=False)
to_csv()