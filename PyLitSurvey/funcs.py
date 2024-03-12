import pandas as pd

def abstract_inverted_index2abstract(abstract_inverted_index):
    indexs = {}
    for word, index in abstract_inverted_index.items():
        for i in index:
            indexs[i] = word
    return ' '.join([word for i, word in sorted(indexs.items())])

def to_str(txt):
    if txt is None:
        return ''
    if isinstance(txt,dict):
        return ''
    if not isinstance(txt,str):
        return str(txt)
    return txt

def substituir_none_por_dict(dicionario):
    for chave, valor in dicionario.items():
        if isinstance(valor, dict):
            substituir_none_por_dict(valor)
        elif isinstance(valor, list):
            for i, item in enumerate(valor):
                if isinstance(item, dict):
                    substituir_none_por_dict(item)
                elif item is None:
                    valor[i] = {}
        elif valor is None:
            dicionario[chave] = {}
    return dicionario


def to_row(doc):
    doc = substituir_none_por_dict(doc)
    _doc = {
        'id':doc.get("_id",''),
        'display_name': doc.get("display_name",''),
        'publication_date': doc.get("publication_date",''),
        'relevance_score': doc.get("relevance_score",''),
        'primary_location_landing_page_url': doc.get("primary_location",{}).get("landing_page_url",''),
        'primary_location_pdf_url': doc.get("primary_location",{}).get("pdf_url",''),
        'primary_location_is_oa': doc.get("primary_location",{}).get("is_oa",''),
        'primary_location_version': doc.get("primary_location",{}).get("version",''),
        'primary_location_license': doc.get("primary_location",{}).get("license",''),
        'cited_by_count': doc.get("cited_by_count",''),
        'doi': doc.get("doi",''),
        'publication_year': doc.get("publication_year",''),
        'cited_by_api_url': doc.get("cited_by_api_url",''),
        'type': doc.get("type",''),
        'is_paratext': doc.get("is_paratext",''),
        'is_retracted': doc.get("is_retracted",''),
        'biblio_issue': doc.get("biblio",{}).get("issue",''),
        'biblio_first_page': doc.get("biblio",{}).get("first_page",''),
        'biblio_volume': doc.get("biblio",{}).get("volume",''),
        'biblio_last_page': doc.get("biblio",{}).get("last_page",''),
        'referenced_works': "|".join(doc.get("referenced_works",{}).get("referenced_works",[])),
        'related_works': "|".join(doc.get("related_works",{}).get("related_works",[])),
        'best_oa_location_source_host_organization': doc.get("best_oa_location",{}).get("source",{}).get("host_organization",''),
        'best_oa_location_source_host_organization_lineage_names': '"|".join(doc.get("best_oa_location",{}).get("source",{}).get("host_organization_lineage_names",{}).get("host_organization_lineage_names",[]))',
        'cited_by_percentile_year_min': doc.get("cited_by_percentile_year",{}).get("min",''),
        'primary_topic_domain_display_name': doc.get("primary_topic",{}).get("domain",{}).get("display_name",''),
        'corresponding_author_ids': '"|".join(doc.get("corresponding_author_ids",{}).get("corresponding_author_ids",[]))',
        'best_oa_location_source_issn': '"|".join(doc.get("best_oa_location",{}).get("source",{}).get("issn",{}).get("issn",[]))',
        'best_oa_location_license': doc.get("best_oa_location",{}).get("license",''),
        'apc_list_currency': doc.get("apc_list",{}).get("currency",''),
        'primary_location_source_host_organization_lineage_names': '"|".join(doc.get("primary_location",{}).get("source",{}).get("host_organization_lineage_names",{}).get("host_organization_lineage_names",[]))',
        'primary_location_source_is_oa': doc.get("primary_location",{}).get("source",{}).get("is_oa",''),
        'primary_location_is_published': doc.get("primary_location",{}).get("is_published",''),
        'best_oa_location_landing_page_url': doc.get("best_oa_location",{}).get("landing_page_url",''),
        'ids_doi': doc.get("ids",{}).get("doi",''),
        'cited_by_percentile_year_max': doc.get("cited_by_percentile_year",{}).get("max",''),
        'best_oa_location_is_published': doc.get("best_oa_location",{}).get("is_published",''),
        'apc_list_value_usd': doc.get("apc_list",{}).get("value_usd",''),
        'primary_topic_display_name': doc.get("primary_topic",{}).get("display_name",''),
        'institutions_distinct_count': doc.get("institutions_distinct_count",''),
        'ids_openalex': doc.get("ids",{}).get("openalex",''),
        'primary_topic_subfield_id': doc.get("primary_topic",{}).get("subfield",{}).get("id",''),
        'language': doc.get("language",''),
        'best_oa_location_source_is_in_doaj': doc.get("best_oa_location",{}).get("source",{}).get("is_in_doaj",''),
        'primary_topic_field_display_name': doc.get("primary_topic",{}).get("field",{}).get("display_name",''),
        'fulltext_origin': doc.get("fulltext_origin",''),
        'open_access_any_repository_has_fulltext': doc.get("open_access",{}).get("any_repository_has_fulltext",''),
        'best_oa_location_is_oa': doc.get("best_oa_location",{}).get("is_oa",''),
        'best_oa_location_source_is_oa': doc.get("best_oa_location",{}).get("source",{}).get("is_oa",''),
        'primary_topic_id': doc.get("primary_topic",{}).get("id",''),
        'title': doc.get("title",''),
        'primary_topic_score': doc.get("primary_topic",{}).get("score",''),
        'apc_list_value': doc.get("apc_list",{}).get("value",''),
        'best_oa_location_source_issn_l': doc.get("best_oa_location",{}).get("source",{}).get("issn_l",''),
        'indexed_in': '"|".join(doc.get("indexed_in",{}).get("indexed_in",[]))',
        'best_oa_location_pdf_url': doc.get("best_oa_location",{}).get("pdf_url",''),
        'best_oa_location_source_display_name': doc.get("best_oa_location",{}).get("source",{}).get("display_name",''),
        'primary_topic_field_id': doc.get("primary_topic",{}).get("field",{}).get("id",''),
        'primary_location_source_issn_l': doc.get("primary_location",{}).get("source",{}).get("issn_l",''),
        'apc_list_provenance': doc.get("apc_list",{}).get("provenance",''),
        'apc_paid_provenance': doc.get("apc_paid",{}).get("provenance",''),
        'primary_topic_subfield_display_name': doc.get("primary_topic",{}).get("subfield",{}).get("display_name",''),
        'countries_distinct_count': doc.get("countries_distinct_count",''),
        'type_crossref': doc.get("type_crossref",''),
        'has_fulltext': doc.get("has_fulltext",''),
        'primary_location_source_id': doc.get("primary_location",{}).get("source",{}).get("id",''),
        'open_access_is_oa': doc.get("open_access",{}).get("is_oa",''),
        'apc_paid_value': doc.get("apc_paid",{}).get("value",''),
        'best_oa_location_source_type': doc.get("best_oa_location",{}).get("source",{}).get("type",''),
        'ngrams_url': doc.get("ngrams_url",''),
        'primary_location_source_is_in_doaj': doc.get("primary_location",{}).get("source",{}).get("is_in_doaj",''),
        'apc_paid_currency': doc.get("apc_paid",{}).get("currency",''),
        'best_oa_location_source_id': doc.get("best_oa_location",{}).get("source",{}).get("id",''),
        'referenced_works_count': doc.get("referenced_works_count",''),
        'best_oa_location_source_host_organization_lineage': '"|".join(doc.get("best_oa_location",{}).get("source",{}).get("host_organization_lineage",{}).get("host_organization_lineage",[]))',
        'primary_location_source_host_organization_lineage': '"|".join(doc.get("primary_location",{}).get("source",{}).get("host_organization_lineage",{}).get("host_organization_lineage",[]))',
        'best_oa_location_version': doc.get("best_oa_location",{}).get("version",''),
        'created_date': doc.get("created_date",''),
        'best_oa_location_is_accepted': doc.get("best_oa_location",{}).get("is_accepted",''),
        'corresponding_institution_ids': "|".join(doc.get("corresponding_institution_ids",{}).get("corresponding_institution_ids",[])),
        'primary_location_source_host_organization': doc.get("primary_location",{}).get("source",{}).get("host_organization",''),
        'primary_location_source_issn': "|".join(doc.get("primary_location",{}).get("source",{}).get("issn",{}).get("issn",[])),
        'apc_paid_value_usd': doc.get("apc_paid",{}).get("value_usd",''),
        'best_oa_location_source_host_organization_name': doc.get("best_oa_location",{}).get("source",{}).get("host_organization_name",''),
        'updated_date': doc.get("updated_date",''),
        'primary_location_source_host_organization_name': doc.get("primary_location",{}).get("source",{}).get("host_organization_name",''),
        'primary_topic_domain_id': doc.get("primary_topic",{}).get("domain",{}).get("id",''),
        'primary_location_source_display_name': doc.get("primary_location",{}).get("source",{}).get("display_name",''),
        'primary_location_source_type': doc.get("primary_location",{}).get("source",{}).get("type",''),
        'primary_location_is_accepted': doc.get("primary_location",{}).get("is_accepted",''),
        'locations_count': doc.get("locations_count",''),
        'author_ids':'|'.join([to_str(tmp.get('author',{}).get('id','')) for tmp in doc.get('authorships',{})]),
        'author_institution_ids':'|'.join([to_str(inst.get('id')) for tmp in all_data[0].get('authorships',{}) for inst in tmp.get('institutions',[]) ]),
        'author_institution_names':'|'.join([to_str(inst.get('display_name')) for tmp in all_data[0].get('authorships',{}) for inst in tmp.get('institutions',[]) ]),
        'author_names': '|'.join([to_str(tmp.get('author',{}).get('display_name','')) for tmp in doc.get('authorships',{})]),
        'author_orcids': '|'.join([to_str(tmp.get('author',{}).get('orcid','')) for tmp in doc.get('authorships',{})]),
        'authorships_author_position': '|'.join([to_str(tmp.get('author_position')) for tmp in doc.get('authorships',{})]),
        'authorships_is_corresponding':'|'.join([to_str(tmp.get('is_corresponding')) for tmp in doc.get('authorships',{})]),
        'authorships_raw_affiliation_string':'|'.join([to_str(tmp.get('raw_affiliation_string')) for tmp in doc.get('authorships',{})]),
        'concept_ids':'|'.join([to_str(tmp.get('id',{})) for tmp in doc.get('concepts',{})  ]),
        'concepts_display_name':'|'.join([to_str(tmp.get('display_name',{})) for tmp in doc.get('concepts',{})  ]),
        'concepts_id':'|'.join([to_str(tmp.get('id',{})) for tmp in doc.get('concepts',{})  ]),
        'concepts_level':'|'.join([to_str(tmp.get('level',{})) for tmp in doc.get('concepts',{})  ]),
        'concepts_score':'|'.join([to_str(tmp.get('score',{})) for tmp in doc.get('concepts',{})  ]),
        'concepts_wikidata':'|'.join([to_str(tmp.get('wikidata',{})) for tmp in doc.get('concepts',{})  ]),
        'counts_by_year_cited_by_count':'|'.join([to_str(tmp.get('cited_by_count',{})) for tmp in doc.get('counts_by_year',{})  ]),
        'counts_by_year_year':'|'.join([to_str(tmp.get('year',{})) for tmp in doc.get('counts_by_year',{})  ]),
        'keywords_keyword':'|'.join([to_str(tmp.get('keyword')) for tmp in doc.get('keywords',{})]),
        'keywords_score':'|'.join([to_str(tmp.get('score')) for tmp in doc.get('keywords',{})]),
        'locations_is_accepted':'|'.join([to_str(tmp.get('is_accepted')) for tmp in doc.get('locations',{})]),
        'locations_is_oa':'|'.join([to_str(tmp.get('is_oa')) for tmp in doc.get('locations',{})]),
        'locations_is_published':'|'.join([to_str(tmp.get('is_published')) for tmp in doc.get('locations',{})]),
        'locations_landing_page_url':'|'.join([to_str(tmp.get('landing_page_url')) for tmp in doc.get('locations',{})]),
        'locations_license':'|'.join([to_str(tmp.get('license')) for tmp in doc.get('locations',{})]),
        'locations_pdf_url':'|'.join([to_str(tmp.get('pdf_url')) for tmp in doc.get('locations',{})]),
        'locations_source':'|'.join([to_str(tmp.get('source',{}).get('display_name','')) for tmp in doc.get('locations',{})]),
        'locations_version':'|'.join([to_str(tmp.get('version',{})) for tmp in doc.get('locations',{})  ]),
        'primary_location_display_name':doc.get('primary_location',{}).get('source',{}).get('display_name','') ,
        'primary_location_host_organization':doc.get('primary_location',{}).get('source',{}).get('host_organization','') ,
        'primary_location_id':doc.get('primary_location',{}).get('source',{}).get('id',''),
        'primary_location_issn_l':doc.get('primary_location',{}).get('source',{}).get('issn_l',''),
        'primary_location_issns':doc.get('primary_location',{}).get('source',{}).get('issns',''),
        'primary_location_type':doc.get('primary_location',{}).get('source',{}).get('type',''),
        'grants_award_id':'|'.join([to_str(tmp.get('award_id','')) for tmp in doc.get('grants',{})]),
        'grants_funder':'|'.join([to_str(tmp.get('funder','')) for tmp in doc.get('grants',{})]),
        'grants_funder_display_name':'|'.join([to_str(tmp.get('funder_display_name','')) for tmp in doc.get('grants',{})]),
        'is_authors_truncated':doc.get('open_access',False),
        'is_oa':doc.get('open_access',{}).get('is_oa',False),
        'mag':doc.get('ids',{}).get('mag',''),
        'pmcid':doc.get('ids',{}).get('pmcid',''),
        'pmid':doc.get('ids',{}).get('pmid',''),
        'mesh_descriptor_name':'|'.join([to_str(tmp.get('descriptor_name','')) for tmp in doc.get('mesh',{})]),
        'mesh_descriptor_ui':'|'.join([to_str(tmp.get('descriptor_ui','')) for tmp in doc.get('mesh',{})]),
        'mesh_is_major_topic':'|'.join([to_str(tmp.get('is_major_topic','')) for tmp in doc.get('mesh',{})]),
        'mesh_qualifier_name':'|'.join([to_str(tmp.get('qualifier_name','')) for tmp in doc.get('mesh',{})]),
        'mesh_qualifier_ui':'|'.join([to_str(tmp.get('qualifier_ui','')) for tmp in doc.get('mesh',{})]),
        'oa_status':doc.get('open_access',{}).get('oa_status',''),
        'oa_url':doc.get('open_access',{}).get('oa_url',''),
        'sustainable_development_goals_display_name':'|'.join([to_str(tmp.get('display_name',{})) for tmp in doc.get('sustainable_development_goals',{})]),
        'sustainable_development_goals_id':'|'.join([to_str(tmp.get('id','')) for tmp in doc.get('sustainable_development_goals',{})]),
        'sustainable_development_goals_score':'|'.join([to_str(tmp.get('score','')) for tmp in doc.get('sustainable_development_goals',{})]),
        'topics_display_name':'|'.join([to_str(tmp.get('display_name','')) for tmp in doc.get('topics',{})]),
        'topics_id':'|'.join([to_str(tmp.get('id','')) for tmp in doc.get('topics',{})]),
        'topics_score':'|'.join([to_str(tmp.get('score','')) for tmp in doc.get('topics',{})]),
    }
    for chave, valor in _doc.items():
        if isinstance(valor,dict):
            _doc[chave] = pd.NA
    return _doc