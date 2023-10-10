import shutil

from PyLitSurvey.config import logger


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