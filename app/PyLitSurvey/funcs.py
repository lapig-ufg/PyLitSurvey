import shutil

from app.PyLitSurvey.config import logger


def count_keys(text) -> dict:
    _count_keys = [
        'Conversion factor',
        'GPP',
        'Gross Primary Productivity',
        'GPP measurements',
        'Plant photosynthesis data',
        'Primary production data',
        'Ecosystem productivity',
        'Carbon fixation rates',
        'Vegetation productivity',
        'Dry biomass',
        'Photosynthetic activity',
        'NPP',
        'Net Primary Productivity',
        'NPP measurements',
        'Biomass accumulation',
        'Ecosystem energy',
        'Net carbon',
        'Plant respiration',
        'LUE',
        'fAPAR',
        'PAR',
        'NPP/GPP ratios',
    ]
    count = {}

    for key in _count_keys:
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
