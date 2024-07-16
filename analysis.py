from pymongo import MongoClient
import matplotlib.pyplot as plt
from PyLitSurvey.config import settings

# Conectando ao MongoDB
client = MongoClient(settings.MONGO_URI)
db = client[f'biblimetry_{settings.VERSION}']
colecao = db['works']

# 1. Distribuição de publicações por ano
publications_per_year = list(colecao.aggregate([
    {"$group": {"_id": "$publication_year", "count": {"$sum": 1}}},
    {"$sort": {"_id": 1}}
]))

# 2. Distribuição de publicações por idioma
publications_per_language = list(colecao.aggregate([
    {"$group": {"_id": "$language", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}}
]))

# 3. Principais autores e suas contagens de publicações
top_authors = list(colecao.aggregate([
    {"$unwind": "$authorships"},
    {"$group": {"_id": "$authorships.author.display_name", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}},
    {"$limit": 10}
]))

# 4. Principais instituições e suas contagens de publicações
top_institutions = list(colecao.aggregate([
    {"$unwind": "$authorships"},
    {"$unwind": "$authorships.institutions"},
    {"$group": {"_id": "$authorships.institutions.display_name", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}},
    {"$limit": 10}
]))

# 5. Distribuição de tópicos ou palavras-chave
# Supondo que a chave para palavras-chave é 'concepts'
top_concepts = list(colecao.aggregate([
    {"$unwind": "$concepts"},
    {"$group": {"_id": "$concepts.display_name", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}},
    {"$limit": 10}
]))

# Função para plotar e salvar gráficos
def plot_bar(data, title, xlabel, ylabel, rotation=0, horizontal=False, filename=None):
    labels = [entry['_id'] for entry in data]
    counts = [entry['count'] for entry in data]
    plt.figure(figsize=(10, 6))
    if horizontal:
        plt.barh(labels, counts)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
    else:
        plt.bar(labels, counts)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(rotation=rotation)
    plt.tight_layout()
    if filename:
        plt.savefig(filename, format='png')
    plt.show()

# 1. Distribuição de publicações por ano
plot_bar(publications_per_year, 'Distribuição de Publicações por Ano', 'Ano', 'Número de Publicações', rotation=45, filename='distribuicao_publicacoes_por_ano.png')

# 2. Distribuição de publicações por idioma
plot_bar(publications_per_language, 'Distribuição de Publicações por Idioma', 'Idioma', 'Número de Publicações', rotation=45, filename='distribuicao_publicacoes_por_idioma.png')

# 3. Principais autores e suas contagens de publicações
plot_bar(top_authors, 'Principais Autores por Número de Publicações', 'Número de Publicações', 'Autor', horizontal=True, filename='principais_autores.png')

# 4. Principais instituições e suas contagens de publicações
plot_bar(top_institutions, 'Principais Instituições por Número de Publicações', 'Número de Publicações', 'Instituição', horizontal=True, filename='principais_instituicoes.png')

# 5. Distribuição de tópicos ou palavras-chave
plot_bar(top_concepts, 'Principais Conceitos por Número de Publicações', 'Número de Publicações', 'Conceito', horizontal=True, filename='principais_conceitos.png')
