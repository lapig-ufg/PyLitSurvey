import sys

from loguru import logger
from dynaconf import Dynaconf
from nltk.corpus import stopwords

settings = Dynaconf(
    envvar_prefix='PYLIT',
    settings_files=[
        'settings.toml',
        '.secrets.toml',
        '../settings.toml',
        '/data/settings.toml',
    ],
    environments=True,
    load_dotenv=True,
)

select = [
    'id',
    'doi',
    'title',
    'abstract_inverted_index',
    'relevance_score',
    'publication_date',
    'language',
    'primary_location',
    'type',
    'type_crossref',
    'open_access',
    'authorships',
    'countries_distinct_count',
    'institutions_distinct_count',
    'corresponding_author_ids',
    'corresponding_institution_ids',
    'apc_list',
    'apc_paid',
    'is_authors_truncated',
    'cited_by_count',
    'biblio',
    'is_retracted',
    'is_paratext',
    'concepts',
    'mesh',
    'locations_count',
    'locations',
    'best_oa_location',
    'sustainable_development_goals',
    'grants',
    'referenced_works_count',
    'referenced_works',
    'related_works',
    'ngrams_url',
    'cited_by_api_url',
    'counts_by_year',
    'updated_date',
    'created_date',
]

stop_words = (
    set(stopwords.words('portuguese'))
    | set(stopwords.words('english'))
    | {
        'http',
        'https',
        'et',
        'et.',
        'al',
        'al,',
        '(',
        ')',
        '0',
        '1',
        '2',
        '3',
        '4',
        '5',
        '6',
        '7',
        '8',
        '9',
        '!',
        '@',
        '#',
        '$',
        '%',
        '^',
        '&',
        '*',
        '(',
        ')',
        '-',
        '_',
        '+',
        '=',
        '/',
        '\\',
        '|',
        ':',
        ';',
        ',',
        '.',
        '?',
        '<',
        '>',
        '[',
        ']',
        '{',
        '}',
        "'",
        '"',
        '`',
        '~',
    }
)


if settings.DEBUG is False:
    logger.remove()
    logger.add(
        sys.stderr,
        level='INFO',
        format='[ {time} | process: {process.id} | {level: <8}] {module}.{function}:{line} {message}',
    )

logger.add(
    './logs/bibil.log',
    rotation='500 MB',
    level='INFO',
)
