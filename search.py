from elasticsearch import Elasticsearch

client = Elasticsearch()
indexName = "medical"
docType = "diseases"
searchFrom = 0
searchSize = 3
# searchBody={
# "fields":["name"],
# "query":{
#     "simple_query_string" : {
#         "query": '+fatigue+fever+"joint pain"',
#         "fields": ["fulltext","title^5","name^10"]
#         }
#     }
# }
# client.search(index=indexName,doc_type=docType, body=searchBody, from_ = searchFrom, size=searchSize)

# searchBody={
# "fields":["name"],
# "query":{
#     "simple_query_string" : {
#         "query": '+fatigue+fever+"joint pain"+rash',
#         "fields": ["fulltext","title^5","name^10"]
#         }
#     }
# }
# client.search(index=indexName,doc_type=docType, body=searchBody, from_ = searchFrom, size=searchSize)
#
# searchBody={
# "fields":["name"],
# "query":{
#     "simple_query_string" : {
#         "query": 'lupsu~2  ',
#         "fields": ["name^10"],
#         }
#     }
# }
# client.search(index=indexName,doc_type=docType, body=searchBody, from_ = searchFrom, size=searchSize)

# searchBody={
# "fields":["name"],
# "query":{
#     "simple_query_string" : {
#         "query": '+"left arm pain"~10',
#         "fields": ["fulltext","title^5","name^10"]
#         }
#     },
# "highlight" : {
#         "fields" : {
#             "fulltext" : {}
#         }
#     }
# }
# client.search(index=indexName,doc_type=docType, body=searchBody, from_ = searchFrom, size=searchSize)

# searchBody={
# "fields":["name"],
# "query":{
#     "simple_query_string" : {
#         "query": 'thirst "weight loss"',
#         "fields": ["fulltext","title^5","name^10"]
#         }
#     }
# }
# client.search(index=indexName,doc_type=docType, body=searchBody, from_ = searchFrom, size=searchSize)
searchBody = {
    "fields": ["name"],
    "query": {
        "filtered": {
            "filter": {
                'term': {'name': 'diabetes'}
            }
        }
    },
    "aggregations": {
        "DiseaseKeywords": {
            "significant_terms": {"field": "fulltext", "size": 30}
        }
    }
}
client.search(index=indexName, doc_type=docType, body=searchBody, from_=searchFrom, size=searchSize)

client = Elasticsearch()
indexName = "medical"
docType = "diseases2"
searchFrom = 0
searchSize = 3

searchBody = {
    "fields": ["name"],
    "query": {
        "filtered": {
            "filter": {
                'term': {'name': 'diabetes'}
            }
        }
    },
    "aggregations": {
        "DiseaseKeywords": {
            "significant_terms": {"field": "fulltext", "size": 30}
        },
        "DiseaseBigrams": {
            "significant_terms": {"field": "fulltext.shingles", "size": 30}
        }
    }
}
client.search(index=indexName, doc_type=docType, body=searchBody, from_=searchFrom, size=searchSize)
