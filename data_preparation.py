import json

from elasticsearch import Elasticsearch

client = Elasticsearch()
indexName = "gastronomical"
docType = 'recipes'

client.indices.create(index=indexName)

file_name = './recipes.json'
recipeMapping = {
    'properties': {
        'name': {'type': 'string'},
        'ingredients': {'type': 'string'}
    }
}
client.indices.put_mapping(index=indexName, doc_type=docType, body=recipeMapping)

with open(file_name) as data_file:
    recipeData = json.load(data_file)

for recipe in recipeData:
    client.index(index=indexName, doc_type=docType, id=recipe['_id']['$oid'],
                 body={"name": recipe['name'], "ingredients": recipe['ingredients']})
