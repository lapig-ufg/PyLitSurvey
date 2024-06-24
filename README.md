# PyLitSurvey

## O arquivo `settings.toml` é utilizado para configurar variáveis e parâmetros importantes para a execução dos scripts da aplicação PyLitSurvey. Abaixo, é fornecida uma descrição detalhada de cada configuração presente no arquivo.

## Configurações

### `DEBUG`

- **Tipo**: Booleano
- **Descrição**: Define se o modo de depuração está ativado.
- **Valor**: 
  - `true`: O modo de depuração está ativado, o que pode fornecer informações adicionais para depuração e desenvolvimento.
  - `false`: O modo de depuração está desativado.

### `QUERY`

- **Tipo**: String
- **Descrição**: A consulta utilizada para pesquisar trabalhos acadêmicos.
- **Valor**: 
  - `"grazing land" OR pastureland OR pasture OR rangeland OR grassland OR savanna OR savannah OR shrubland OR "forage crop" OR "perennial forage"`: Esta consulta busca por documentos que contenham qualquer um dos termos listados relacionados a terras de pastagem e vegetação similar.

### `FILTER_LANG`

- **Tipo**: String
- **Descrição**: Filtro de idioma para os resultados da consulta.
- **Valor**: 
  - `'en|pt|fr|es'`: Filtra os resultados para incluir apenas documentos escritos em inglês (`en`), português (`pt`), francês (`fr`) e espanhol (`es`).

### `MAXYEAR`

- **Tipo**: String
- **Descrição**: Ano máximo de publicação dos documentos a serem considerados.
- **Valor**: 
  - `'-2023'`: Considera apenas documentos publicados até o ano de 2023.

### `VERSION`

- **Tipo**: String
- **Descrição**: Versão da configuração ou do banco de dados a ser utilizado.
- **Valor**: 
  - `'001'`: A versão atual é `001`.

### `CORES`

- **Tipo**: Inteiro
- **Descrição**: Número de núcleos de CPU a serem utilizados para processamento paralelo.
- **Valor**: 
  - `48`: Utiliza 48 núcleos de CPU para otimizar o desempenho das operações de processamento.

## Exemplo de Uso

O arquivo `settings.toml` deve ser colocado no diretório de configuração da aplicação PyLitSurvey. Durante a execução dos scripts, essas configurações são carregadas para ajustar a operação de acordo com os parâmetros especificados.

```toml
[default]
DEBUG=true
QUERY='"grazing land" OR pastureland OR pasture OR rangeland OR grassland OR savanna OR savannah OR shrubland OR "forage crop" OR "perennial forage"'
FILTER_LANG='en|pt|fr|es'
MAXYEAR='-2023'
VERSION='001'
CORES=48

# Documentação do Script `get_lit.py`

O script `get_lit.py`, que busca trabalhos acadêmicos da API OpenAlex, processa esses dados e os insere em uma coleção MongoDB.

## Pré-requisitos

Certifique-se de ter as seguintes bibliotecas instaladas:

- `pymongo`
- `pyalex`
- `tqdm`
- `PyLitSurvey`

## Configuração

### Importações

O script utiliza as seguintes bibliotecas:

- `pymongo` para interagir com o MongoDB.
- `pyalex` para buscar dados da API OpenAlex.
- `tqdm` para exibir uma barra de progresso.
- `PyLitSurvey.config` para carregar configurações e o logger.

### Configuração da Consulta

1. **Criar a consulta à API do OpenAlex**:
   - A consulta é criada usando a biblioteca `pyalex` com os parâmetros definidos em `settings.QUERY` e `settings.FILTER_LANG`.
   
2. **Contar o número total de documentos que a consulta retornará**:
   - O método `count()` é usado para obter o total de documentos.

3. **Configurar o número de documentos processados por iteração**:
   - A variável `ITER_PER_STEP` define quantos documentos serão processados em cada iteração (neste caso, 200).

4. **Registrar o número total de documentos**:
   - O logger é utilizado para registrar o total de documentos a serem processados.

### Processamento e Inserção no MongoDB

1. **Barra de Progresso**:
   - A barra de progresso é criada usando `tqdm` e é configurada com o total de iterações.

2. **Conectar ao MongoDB**:
   - O script se conecta ao MongoDB utilizando a URI definida em `settings.MONGO_URI`.

3. **Selecionar o Banco de Dados e a Coleção**:
   - O banco de dados e a coleção são selecionados com base nas configurações.

4. **Iterar sobre os Documentos**:
   - Os documentos são paginados e processados em lotes de 200.

5. **Processar Documentos**:
   - Cada documento é preparado para inserção, incluindo a modificação do campo `id` para `_id`.

6. **Inserir Documentos no MongoDB**:
   - **Inserção em Massa**:
     - O script tenta inserir todos os documentos do lote de uma vez.
   
   - **Inserção Individual em Caso de Falha**:
     - Se a inserção em massa falhar, o script tenta inserir os documentos individualmente.
     - O logger registra se um documento já existe no banco de dados para evitar duplicações.
     - Quaisquer outras exceções são registradas para análise posterior.

7. **Atualizar a Barra de Progresso**:
   - A barra de progresso é atualizada a cada 200 documentos processados.

## Logs e Erros

- **Duplicação de Chaves**:
  - Se um documento já existir no MongoDB, será registrado um aviso no logger indicando o ID do documento duplicado.

- **Outras Exceções**:
  - Qualquer outra exceção será registrada no logger para facilitar a análise e correção de erros.

## Conclusão

O script `get_lit.py` permite a importação eficiente de grandes quantidades de dados acadêmicos da API OpenAlex para um banco de dados MongoDB, lidando com a duplicação de chaves e fornecendo feedback em tempo real através de uma barra de progresso.


# Documentação do Script `to_csv.py`

Que filtra, processa e exporta dados de trabalhos acadêmicos de um banco de dados MongoDB para arquivos CSV.

## Pré-requisitos

Certifique-se de ter as seguintes bibliotecas instaladas:

- `pandas`
- `pymongo`
- `PyLitSurvey`

## Configuração

### Importações

O script utiliza as seguintes bibliotecas:

- `pandas` para manipulação de dados.
- `pymongo` para interagir com o MongoDB.
- `PyLitSurvey.funcs` para funções utilitárias como `to_row` e `abstract_inverted_index2abstract`.
- `PyLitSurvey.config` para carregar configurações e o logger.

### Configuração Inicial

1. **Carregar Dados Médicos**:
   - O arquivo `med.csv` é carregado em um DataFrame `MED`.

2. **Inicializar Listas**:
   - `SOUCER` e `SOUCER_ID` são listas inicializadas para armazenar dados de fontes.

## Funções

### `filter_by_issn(locations)`

Esta função filtra informações de locais baseadas no ISSN.

- **Parâmetros**:
  - `locations` (list): Lista de dicionários contendo informações de locais.

- **Retorna**:
  - Uma tupla com nomes de exibição, IDs de fontes, ISSNs e um indicador se a fonte está na lista médica.

- **Processo**:
  - Itera sobre cada local, extrai informações da fonte e verifica se a fonte está na lista médica (`MED`).
  - Atualiza listas globais (`SOUCER`, `SOUCER_ID`) para evitar duplicações.
  - Retorna uma string concatenada de nomes de exibição, IDs de fontes, ISSNs e indicadores médicos.

### `to_csv_all_columns()`

Esta função exporta todos os documentos do MongoDB para um CSV, incluindo todas as colunas.

- **Processo**:
  - Conecta ao MongoDB e seleciona a coleção `works`.
  - Itera sobre os documentos em blocos de 10.000.
  - Concatena os dados em um DataFrame e exporta para `output/all_columns.csv`.

### `dict_to_row_short(doc)`

Esta função converte um documento do MongoDB em uma linha de DataFrame.

- **Parâmetros**:
  - `doc` (dict): Dicionário contendo dados do documento.

- **Retorna**:
  - Um dicionário representando uma linha do DataFrame.

- **Processo**:
  - Chama `filter_by_issn` para obter informações de locais.
  - Monta uma linha com campos específicos do documento.
  - Adiciona um campo `abstract` convertido se disponível.
  - Adiciona campos de palavras-chave se disponíveis.

### `to_csv()`

Esta função exporta documentos filtrados do MongoDB para um CSV, incluindo apenas colunas específicas.

- **Processo**:
  - Conecta ao MongoDB e seleciona a coleção `works`.
  - Itera sobre os documentos filtrados por tipo e palavras-chave em blocos de 10.000.
  - Concatena os dados em um DataFrame e exporta para `output/nomed_filtrado.csv`.
  - Exporta a lista de fontes para `output/soucer.csv`.

## Logs e Erros

- **Exceções**:
  - O logger registra exceções ocorridas durante o processamento de locais e ao converter documentos.
  - Exceções são levantadas com mensagens apropriadas para facilitar a depuração.

## Conclusão

O script `to_csv.py` permite a exportação eficiente de dados acadêmicos filtrados de um banco de dados MongoDB para arquivos CSV, lidando com a verificação de fontes e a inclusão de campos relevantes de forma organizada.
