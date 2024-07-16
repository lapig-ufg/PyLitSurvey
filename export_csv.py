from pymongo import MongoClient
import pandas as pd

# Conectar ao MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client['biblimetry_001']  # Substitua pelo nome do banco de dados
colecao = db['works']  # Substitua pelo nome da coleção

# Ler os documentos da coleção
docs = list(colecao.find())

# Converter os documentos em um DataFrame do Pandas
df = pd.DataFrame(docs)

# Exportar o DataFrame para um arquivo CSV
df.to_csv('exported_data.csv', index=False)

print("Exportação concluída com sucesso!")